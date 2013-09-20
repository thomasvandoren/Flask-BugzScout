#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Verify Flask-BugzScout behavior."""

from __future__ import print_function, unicode_literals

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

    def test_init(self):
        """Verify constructor calls through to init_app instance method."""
        self.fail('no')

    def test_init_app__defaults(self):
        """Verify init_app sets defaults for app configuration and configures
        error handlers.
        """
        self.fail('no')

    def test_init_app(self):
        """Verify init_app uses app configuration."""
        self.fail('no')

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
        self.fail('no')

    def test_app_from_context__context(self):
        """Verify _app_from_context works when context is a context."""
        self.fail('no')

    def test_app_from_context__none(self):
        """Verify _app_from_context returns top app from flask request context
        when context is None.
        """
        self.fail('no')

    def test_app_from_context__false(self):
        """Verify _app_from_context returns top app from flask request context
        when context is False.
        """
        self.fail('no')

    def test_report_error(self):
        """Verify description and extra are setup and sent to celery."""
        self.fail('no')

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
