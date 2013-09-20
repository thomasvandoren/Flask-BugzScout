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
