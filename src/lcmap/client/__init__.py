"""
The client module provides the class for interacting with the LCMAP service.

The Client class is comprised of components (instances of other objects)
assigned to attributes on the class. Some of these components represent the
high-level architecture of the LCMAP service itself, while others are
supporting components.
"""
import logging

from . import cfg
from . import http
from . import logger

from .api import (auth, compatibility, data, jobs, models,
                  notifications, routes, system, users)


__version__ = "1.0.0-dev"
log = logging.getLogger(__name__)
context = routes.base_context


class Client(object):
    def __init__(self, force_reload=False, colored_logs=True):
        # Primary API components
        self.auth = None
        self.compatibility = None
        self.data = None
        self.jobs = None
        self.models = None
        self.notifications = None
        self.system = None
        self.users = None

        # Supporting components
        self.cfg = None
        self.http = None

        # Initialization
        self.initialize(force_reload=force_reload, colored_logs=colored_logs)

    def initialize(self, force_reload=False, colored_logs=True):
        """Set up the client components.

        This is provided as a separate method from the __init__ used for object
        instantiation in order to reload client components (as necessary) in
        interactive sessions without having to reinstantiate the client object itself.
        Right now, the amount of work done in __init__ is small, but this will
        likely change, adding more value to the chossen approach.
        """
        log.debug("Initializing client components ...")
        log.debug("\tSetting up supporting components ...")
        self.configure(force_reload=force_reload, colored_logs=colored_logs)
        self.http = http.HTTP(cfg=self.cfg)
        log.debug("\tSetting up primary components ...")
        self.auth = auth.Auth(cfg=self.cfg, http=self.http)
        self.compatibility = compatibility.Compatibility(self.http)
        self.data = data.Data(self.http)
        self.jobs = jobs.Jobs(self.http)
        self.models = models.Models(self.http)
        self.notifications = notifications.Notifications(self.http)
        self.system = system.System(self.http)
        self.users = users.Users(self.http)

    def configure(self, force_reload=False, colored_logs=True):
        self.cfg = cfg.Config(force_reload=force_reload, colored_logs=colored_logs)
        logger.configure(self.cfg)

    def reload(self):
        self.configure(force_reload=True, colored_logs=self.cfg.colored_logs)
