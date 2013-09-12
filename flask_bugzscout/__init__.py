#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flask-BugzScout"""


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

        # TODO: Think about this... (thomas, 2013-09-12)
        if not app.testing:
            self.url = app.config['BUGZSCOUT_URL']
            self.user = app.config['BUGZSCOUT_USER']
            self.project = app.config['BUGZSCOUT_PROJECT']
            self.area = app.config['BUGZSCOUT_AREA']

            app.extensions['bugzscout'] = self
