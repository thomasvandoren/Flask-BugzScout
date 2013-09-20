#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask-BugzScout
===============

`BugzScout <https://pypi.python.org/pypi/bugzscout>`_ extension for Flask.
"""

import bugzscout
import flask
import functools
import os
import pkg_resources
import pprint
import sys
import traceback


class BugzScout(object):
    """Recording Flask and HTTP errors to FogBugz via BugzScout."""

    def __init__(self, app=None):
        """Initialize a new BugzScout instance."""
        super(BugzScout, self).__init__()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize BugzScout with Flask app."""

        # Update app extensions.
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        if 'bugzscout' in app.extensions:
            app.logger.warning('Repeated BugzScout initialization attempt.')
            return

        # Configure defaults on app.
        app.config.setdefault('BUGZSCOUT_URL', None)
        app.config.setdefault('BUGZSCOUT_USER', None)
        app.config.setdefault('BUGZSCOUT_PROJECT', None)
        app.config.setdefault('BUGZSCOUT_AREA', None)

        app.config.setdefault('BUGZSCOUT_HTTP_CODES', set(xrange(400, 418)))

        self.url = app.config['BUGZSCOUT_URL']
        self.user = app.config['BUGZSCOUT_USER']
        self.project = app.config['BUGZSCOUT_PROJECT']
        self.area = app.config['BUGZSCOUT_AREA']

        app.handle_exception = self._get_exception_handler(app)
        app.handle_http_exception = self.get_http_exception_handler(app)

        app.extensions['bugzscout'] = self

    def filter(self, resource, resource_type):
        """Filter a dict of data based on the configured filters for its type.

        :type resource: dict
        :arg resource: resource to filter, like headers or cookies

        :type resource_type: str
        :arg resource_type: type of resource to filter

        :rtype: dict
        :returns: filtered resource
        """
        # FIXME: This probably should do something...
        #        (thomasvandoren, 2013-09-19)
        return resource

    def _get_exception_handler(self, app):
        """Create exception handler that wraps app exception handler.

        :type app: Flask app
        :arg app: Flask app to report exceptions to BugzScout
        """
        handle_exception = app.handle_exception

        @functools.wraps(handle_exception)
        def wrapper(exception):
            self._report_error(flask._request_ctx_stack.top)
            return handle_exception(exception)

        return wrapper

    def _get_http_exception_handler(self, app):
        """Create HTTP exception handler that wraps app HTTP exception handler.

        :type app: Flask app
        :arg app: Flask app to report HTTP exceptions to BugzScout
        """
        handle_http_exception = app.handle_http_exception

        @functools.wraps(handle_http_exception)
        def wrapper(exception):
            if exception.code in app.config['BUGZSCOUT_HTTP_CODES']:
                self._report_error(flask._request_ctx_stack.top)
            return handle_http_exception(exception)

        return wrapper

    def _get_app_from_context(self, context):
        """Given a context, which may be None, find and return the current
        flask app.

        :type context: FIXME
        :arg context: FIXME
        """
        if context:
            if isinstance(context, flask.Flask):
                return context
            else:
                return context.app
        else:
            return flask._request_ctx_stack.top.app

    def _report_error(self, context):
        """Report an error to BugzScout!

        :type context: FIXME
        :arg context: FIXME
        """
        app = self._get_app_from_context(context)

        app_data = self._get_app_data(app)
        request_data = self._get_request_data(
            app, context.request, context.session)
        exception_data = self._get_exception_data(*sys.exc_info())

        description = '{method} {url} {summary}'.format(
            request_data['method'],
            request_data['url'],
            exception_data['summary'])

        # FogBugz appears to limit the length of the description (the case
        # title) to ~125 chars, but BugzScout will use the entire description
        # when collating. For now, limit the normalized description to 125
        # chars so the descriptions make sense.
        description = description[:125]

        extra = ''.join([
            '{traceback}',
            '\n\n', '----------', '\n\n',
            'Request:\n'
            '{request_data}',
            '\n\n', '----------', '\n\n',
            'App data:\n',
            '{app_data}',
        ]).format(
            traceback=exception_data['traceback'],
            request_data=pprint.pformat(request_data),
            app_data=pprint.pformat(app_data)
        )

        app.logger.info('Publishing error to BugzScout asynchronously.')
        bugzscout.ext.celery_app.submit_error.delay(
            self.url,
            self.user,
            self.project,
            self.area,
            description,
            extra=extra)

    def _get_exception_data(self, exc_type, exc_value, exc_traceback):
        """Returns dict of exception info, including the full stack trace and a
        summary line.

        :type exc_type: FIXME
        :arg exc_type: FIXME

        :type exc_value: FIXME
        :arg exc_value: FIXME

        :type exc_traceback: FIXME
        :arg exc_traceback: FIXME

        :rtype: dict
        :returns: dict with summary and traceback keys
        """
        tb = traceback.format_exception(
            exc_type, exc_value, exc_traceback)
        summary = '{0}: {1}'.format(str(exc_type.__name__), str(exc_value))
        return {
            'summary': summary,
            'traceback': tb,
        }

    def _get_request_data(self, app, request, session):
        """Returns dict of request data.

        :type app: flask.Flask
        :arg app: Flask application

        :type request: flask.Request
        :arg request: Request instance

        :type session: flask.session
        :arg session: Flask session

        :rtype: dict
        :returns: dict of request data include verb, path, body, etc.
        """
        handler = None
        if hasattr(request, 'blueprint'):
            handler = request.blueprint
        else:
            handler = request.module

        return {
            'method': request.method,
            'url': request.url,
            'headers': self.filter(request.headers, 'headers'),
            'cookies': self.filter(request.cookies, 'cookies'),
            'session': self.filter(session, 'session'),
            'remote_ip': request.remote_addr,
            'body': request.data,
            'handler': handler,
        }

    def _get_app_data(self, app):
        """Returns dict of application data, which may be helpful for
        debugging.

        :type app: flask.Flask
        :arg app: Flask application

        :rtype: dict
        :returns: dict of application, environment, and module data
        """
        # Gather a copy of the app configuration.
        env = app.config.copy()

        # Gather current environment variables, prefix with "os.".
        for key, val in os.environ.iteritems():
            env['os.{0}'.format(key)] = val

        # Gather mapping of module names to versions.
        modules = {}
        for module in pkg_resources.working_set:
            modules[module.name] = module.version

        return {
            'env': self.filter(env, 'configuration'),
            'python_version': sys.version.replace('\n', ''),
            'application_root_directory': app.root_path,
            'loaded_modules': modules,
        }
