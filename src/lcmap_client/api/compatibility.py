import logging

from lcmap_client.api import base, routes


log = logging.getLogger(__name__)

context = routes.compatibility_context


class Compatibility(base.APIComponent):
    ""
