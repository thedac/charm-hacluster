'''
Created on May 14, 2015

@author: wolsen
'''
import logging

from .apidriver import APIDriver

log = logging.getLogger('vmaas.main')


class MAASException(Exception):
    pass


class MAASDriverException(Exception):
    pass


class MAASClient(object):
    """
    A wrapper for the python maas client which makes using the API a bit
    more user friendly.
    """

    def __init__(self, api_url, api_key, **kwargs):
        self.driver = self._get_driver(api_url, api_key, **kwargs)

    def _get_driver(self, api_url, api_key, **kwargs):
        return APIDriver(api_url, api_key)

    def _validate_maas(self):
        try:
            resp = self.driver.validate_maas()
            logging.info("Validated MAAS API")
            return True
        except Exception as e:
            logging.error("MAAS API validation has failed. "
                           "Check maas_url and maas_credentials. Error: {}"
                           "".format(e))
            return False
        
    ###########################################################################
    #  DNS API - http://maas.ubuntu.com/docs2.0/api.html#dnsresource
    ###########################################################################
    def get_dnsresources(self):
        """
        Get a listing of DNS resources which are currently defined.

        :returns: a list of DNS objects
        DNS object is a dictionary of the form:
        {'fqdn': 'keystone.maas',
         'resource_records': [],
         'address_ttl': None,
         'resource_uri': '/MAAS/api/2.0/dnsresources/1/',
         'ip_addresses': [],
         'id': 1}
        """
        resp = self.driver.get_dnsresources()
        if resp.ok:
            return resp.data
        return []

    def update_dnsresource(self, rid, fqdn, ip_address):
        """
        Updates a DNS resource with a new ip_address

        :param rid: The dnsresource_id i.e.
                    /api/2.0/dnsresources/{dnsresource_id}/
        :param fqdn: The fqdn address to update
        :param ip_address: The ip address to update the A record to point to
        :returns: True if the DNS object was updated, False otherwise.
        """
        resp = self.driver.update_dnsresource(rid, fqdn, ip_address)
        if resp.ok:
            return True
        return False

    def create_dnsresource(self, fqdn, ip_address, address_ttl=None):
        """
        Creates a new DNS resource

        :param fqdn: The fqdn address to update
        :param ip_address: The ip address to update the A record to point to
        :param adress_ttl: DNS time to live
        :returns: True if the DNS object was updated, False otherwise.
        """
        resp = self.driver.create_dnsresource(fqdn, ip_address, address_ttl)
        if resp.ok:
            return True
        return False

    ###########################################################################
    #  IP API - http://maas.ubuntu.com/docs2.0/api.html#ip-address
    ###########################################################################
    def get_ipaddresses(self):
        """
        Get a list of ip addresses

        :returns: a list of ip address dictionaries
        """
        resp = self.driver.get_ipaddresses()
        if resp.ok:
            return resp.data
        return []

    def create_ipaddress(self, ip_address, hostname=None):
        """
        Creates a new IP resource

        :param ip_address: The ip address to register
        :param hostname: the hostname to register at the same time
        :returns: True if the DNS object was updated, False otherwise.
        """
        resp = self.driver.create_ipaddress(ip_address, hostname)
        if resp.ok:
            return True
        return False
