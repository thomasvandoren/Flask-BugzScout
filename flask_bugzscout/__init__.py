#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask-BugzScout"""

import flask
import functools


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

        # FIXME: use fogbugz service url by default... (thomas, 2013-09-12)
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

    def _report_error(self, top_of_stack):
        """FIXME!

        :type top_of_stack: FIXME
        :arg top_of_stack: FIXME
        """
        pass
