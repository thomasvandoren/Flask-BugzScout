#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Verify Flask-BugzScout behavior."""

from __future__ import print_function, unicode_literals

import flask
import flask_bugzscout
import mock
import unittest


class BugzScoutTests(unittest.TestCase):
    __doc__ = __doc__

    def setUp(self):
        """Setup some useful mocks."""
        super(BugzScoutTests, self).setUp()
        self.app = mock.Mock(name='app')
        self.app.extensions = {}
        self.app.config = {}

        def noop(*args, **kwargs):
            pass

        self.app.handle_exception = noop
        self.app.handle_http_exception = noop

    def make_bugzscout(self):
        """Create and return an instance of BugzScout."""
        return flask_bugzscout.BugzScout(self.app)

    def test_init(self):
        """Verify constructor calls through to init_app instance method."""
        b = flask_bugzscout.BugzScout(self.app)
        self.assertIsNotNone(b)

    def test_init_app__defaults(self):
        """Verify init_app sets defaults for app configuration and configures
        error handlers.
        """
        b = self.make_bugzscout()

        self.assertIsNone(self.app.config['BUGZSCOUT_URL'])
        self.assertIsNone(self.app.config['BUGZSCOUT_USER'])
        self.assertIsNone(self.app.config['BUGZSCOUT_PROJECT'])
        self.assertIsNone(self.app.config['BUGZSCOUT_AREA'])
        self.assertEqual(
            {x for x in range(400, 418)},
            self.app.config['BUGZSCOUT_HTTP_CODES'])

        self.assertIsNone(b.url)
        self.assertIsNone(b.user)
        self.assertIsNone(b.project)
        self.assertIsNone(b.area)

    def test_init_app(self):
        """Verify init_app uses app configuration."""
        cfg = {
            'BUGZSCOUT_URL': 'http://my.internal/',
            'BUGZSCOUT_USER': 'my-user',
            'BUGZSCOUT_PROJECT': 'my-project',
            'BUGZSCOUT_AREA': 'my-area',
            'BUGZSCOUT_HTTP_CODES': [404, 405],
        }
        self.app.config.update(cfg)
        b = self.make_bugzscout()

        self.assertEqual('http://my.internal/', b.url)
        self.assertEqual('my-user', b.user)
        self.assertEqual('my-project', b.project)
        self.assertEqual('my-area', b.area)
        self.assertEqual(self.app.config['BUGZSCOUT_HTTP_CODES'], [404, 405])

    def test_filter__noop(self):
        """Verify filter is a noop.

        This is by no means desirable. It is a reminder that I need to change
        it!
        """
        self.assertEqual(
            123,
            flask_bugzscout.BugzScout(self.app).filter(123, None))

    def test_app_from_context(self):
        """Verify _app_from_context works when context is type flask.Flask."""
        b = self.make_bugzscout()
        ctx = flask.Flask('__main__')
        actual_app = b._get_app_from_context(ctx)
        self.assertIs(ctx, actual_app)

    def test_app_from_context__context(self):
        """Verify _app_from_context works when context is a context."""
        b = self.make_bugzscout()
        app = flask.Flask('__main__')
        ctx = mock.Mock(name='context')
        ctx.app = app

        actual_app = b._get_app_from_context(ctx)
        self.assertIs(app, actual_app)

    def test_app_from_context__none(self):
        """Verify _app_from_context returns top app from flask request context
        when context is None.
        """
        b = self.make_bugzscout()
        ctx = mock.Mock(name='context')
        app = mock.Mock(name='app')
        ctx.app = app
        flask._request_ctx_stack.push(ctx)

        actual_app = b._get_app_from_context(None)
        self.assertIs(app, actual_app)

    def test_app_from_context__false(self):
        """Verify _app_from_context returns top app from flask request context
        when context is False.
        """
        b = self.make_bugzscout()
        ctx = mock.Mock(name='context')
        app = mock.Mock(name='app')
        ctx.app = app
        flask._request_ctx_stack.push(ctx)

        actual_app = b._get_app_from_context(False)
        self.assertIs(app, actual_app)

    @mock.patch('sys.exc_info')
    @mock.patch('bugzscout.ext.celery_app.submit_error.delay')
    def test_report_error(self, mock_submit, mock_exc_info):
        """Verify description and extra are setup and sent to celery."""
        b = self.make_bugzscout()

        # Setup context.
        ctx = mock.Mock(name='context')
        ctx.app = self.app

        # Return a ValueError.
        mock_exc_info.return_value = (
            ValueError, ValueError('boom!'), None)

        b._report_error(ctx)
        mock_submit.assert_called_once_with(
            b.url,
            b.user,
            b.project,
            b.area,
            mock.ANY,
            extra=mock.ANY)

    def test_get_exception_data(self):
        """Verify summary and traceback are formatted correct for a given
        exception.
        """
        self.fail('no')

    def test_get_request_data(self):
        """Verify _get_request_data works with a non-Blueprinted url."""
        self.fail('no')

    def test_get_request_data__blueprint(self):
        """Verify _get_request_data works with a Blueprint handler."""
        self.fail('no')

    def test_get_app_data(self):
        """Verify _get_app_data returns dict with environment, app, and module
        data.
        """
        self.fail('no')
