#
# Copyright 2015, Canonical Ltd
#
import logging

log = logging.getLogger('vmaas.main')


class Response(object):
    """
    Response for the API calls to use internally
    """
    def __init__(self, ok=False, data=None):
        self.ok = ok
        self.data = data

    def __nonzero__(self):
        """Allow boolean comparison"""
        return bool(self.ok)


class MAASDriver(object):
    """
    Defines the commands and interfaces for generically working with
    the MAAS controllers.
    """

    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def _get_system_id(self, obj):
        """
        Returns the system_id from an object or the object itself
        if the system_id is not found.
        """
        if 'system_id' in obj:
            return obj.system_id
        return obj

    def _get_uuid(self, obj):
        """
        Returns the UUID for the MAAS object. If the object has the attribute
        'uuid', then this method will return obj.uuid, otherwise this method
        will return the object itself.
        """
        if hasattr(obj, 'uuid'):
            return obj.uuid
        else:
            log.warning("Attr 'uuid' not found in %s" % obj)

        return obj
