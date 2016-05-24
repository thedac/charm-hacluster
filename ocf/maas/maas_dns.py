#!/usr/bin/python3

import maasclient
import argparse
import sys
import logging


class MAASDNS(object):
    def __init__(self, options):
        self.maas = maasclient.MAASClient(options.maas_server,
                                          options.maas_credentials)
        # String representation of the fqdn
        self.fqdn = options.fqdn
        # Dictionary representation of MAAS dnsresource object
        # XXX do this as a property
        self.dnsresource = self.get_dnsresource()
        # String representation of the time to live
        self.ttl = str(options.ttl)
        # String representation of the ip
        self.ip = options.ip_address

    def get_dnsresource(self):
        dnsresources = self.maas.get_dnsresources()
        self.dnsresource = None
        for dnsresource in dnsresources:
            if dnsresource['fqdn'] == self.fqdn:
                self.dnsresource = dnsresource
        return self.dnsresource

    def get_dnsresource_id(self):
        return self.dnsresource['id']

    def update_resource(self):
        """ Take in DNS resource ID"""
        return self.maas.update_dnsresource(self.dnsresource['id'],
                                            self.dnsresource['fqdn'],
                                            self.ip)

    def create_dnsresource(self):
        """ Take in DNS resource ID"""
        return self.maas.create_dnsresource(self.fqdn,
                                            self.ip,
                                            self.ttl)


class MAASIP(object):
    def __init__(self, options):
        self.maas = maasclient.MAASClient(options.maas_server,
                                          options.maas_credentials)
        # String representation of the IP
        self.ip = options.ip_address
        # Dictionary representation of MAAS ipaddresss object
        # XXX do this as a property
        self.ipaddress = self.get_ipaddress()

    def get_ipaddress(self):
        ipaddresses = self.maas.get_ipaddresses()
        self.ipaddress = None
        for ipaddress in ipaddresses:
            if ipaddress['ip'] == self.ip:
                self.ipaddress = ipaddress
        return self.ipaddress

    def create_ipaddress(self, hostname=None):
        """ Create ipaddress in MAAS DB"""
        return self.maas.create_ipaddress(self.ip, hostname)


def setup_logging(logfile, log_level='INFO'):
    logFormatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(log_level)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    try:
        fileLogger = logging.getLogger('file')
        fileLogger.propagate = False

        fileHandler = logging.FileHandler(logfile)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)
        fileLogger.addHandler(fileHandler)
    except IOError:
        logging.error('Unable to write to logfile: {}'.format(logfile))


def telco_ha_dns():

    parser = argparse.ArgumentParser()
    parser.add_argument('--maas_server', '-s',
                        help='URL to mangage the MAAS server',
                        required=True)
    parser.add_argument('--maas_credentials', '-c',
                        help='MAAS OAUTH credentials',
                        required=True)
    parser.add_argument('--fqdn', '-d',
                        help='Fully Qualified Domain Name',
                        required=True)
    parser.add_argument('--ip_address', '-i',
                        help='IP Address, target of the A record',
                        required=True)
    parser.add_argument('--ttl', '-t',
                        help='DNS Time To Live in seconds',
                        default='')
    parser.add_argument('--logfile', '-l',
                        help='Path to logfile',
                        default='/var/log/{}.log'
                                ''.format(sys.argv[0]
                                          .split('/')[-1]
                                          .split('.')[0]))
    options = parser.parse_args()

    setup_logging(options.logfile)
    logging.info("Starting maas_dns")

    # XXX If it is necessary to register the IP with MAAS
    # Use the MAASIP object
    """
    ip_obj = MAASIP(options)
    if not ip_obj.ipaddress:
        logging.info('Create the ipaddress')
        # ip_obj.create_ipaddress()
    """

    dns_obj = MAASDNS(options)
    if not dns_obj.dnsresource:
        logging.info('DNS Resource does not exist. '
                     'Create it with the maas cli.')
        #logging.info('Create the dnsresource')
        #dns_obj.create_dnsresource()
    elif dns_obj.dnsresource.get('ip_addresses'):
        for ip in dns_obj.dnsresource['ip_addresses']:
            # XXX What if there are more than one ips? Delete?
            if ip.get('ip') != options.ip_address:
                logging.info('Update the dnsresource with IP: {}'
                             ''.format(options.ip_address))
                dns_obj.update_resource()
            else:
                logging.info('IP is the SAME {}, no update required'
                             ''.format(options.ip_address))
    else:
        logging.info('Update the dnsresource with IP: {}'
                     ''.format(options.ip_address))
        dns_obj.update_resource()


if __name__ == '__main__':
    telco_ha_dns()
