import logging


log = logging.getLogger(__name__)


class APIComponent(object):

    def __init__(self, http):
        self.http = http
        self.initialize()

    def initialize(self):
        pass
