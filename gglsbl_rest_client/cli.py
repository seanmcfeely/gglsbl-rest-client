#!/usr/bin/env python3

import os
import sys
import logging
import argparse
import coloredlogs
import pprint

from gglsbl_rest_client.helpers import load_config
from gglsbl_rest_client import GGLSBL_Rest_Service_Client as GRS_Client

# configure logging #
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s')

logger = logging.getLogger('gglsbl-rest-client')
coloredlogs.install(level='INFO', logger=logger)

def main():
    parser = argparse.ArgumentParser(description="A client for querying MLSec gglsbl-rest Services (https://github.com/mlsecproject)")
    parser.add_argument('-d', '--debug', action="store_true", help="set logging to DEBUG", default=False)
    parser.add_argument('-rh', '--remote-host', action="store", default='127.0.0.1', help='the hostname or IP address where the service is listening. Default is localhost.')
    parser.add_argument('-p', '--port', action='store', default='5000', help='the port the service is listening on. Default: 5000')
    parser.add_argument('-cs', '--check-status', action='store_true', default=False, help='Check the status of the service')
    parser.add_argument('-l','--lookup-url', help='the url to lookup')
    parser.add_argument('--ignore-proxy', action='store_true', default=True, help='ignore system proxy. On by default.')
    args = parser.parse_args()

    if args.debug:
        coloredlogs.install(level='DEBUG', logger=logger)

    config = load_config(required_options=['ignore_proxy', 'remote_host', 'remote_port'])
    if not config:
        sys.exit()
    #override defaults
    args.remote_host = config['remote_host'] if args.remote_host is '127.0.0.1' else args.remote_host
    args.port = config['remote_port'] if args.port is '5000' else args.port
    args.ignore_proxy = config.getBoolean('ignore_proxy') if not args.ignore_proxy else args.ignore_proxy

    if args.ignore_proxy:
        if 'http_proxy' in os.environ:
            logger.debug("Deleteing http_proxy environment variable.")
            del os.environ['http_proxy']

    if not args.remote_host:
        logger.error("Hostname or address of service is required.")
        sys.exit()
    if not args.port:
        logger.error("The port the service is listening on is required.")
        sys.exit()

    # Create a SafeBrowsing Client & make sure there is a connection
    sbc = GRS_Client(args.remote_host, args.port)

    if args.check_status:
        result = sbc.service_status()
        if result:
            pprint.pprint(result)
        sys.exit()

    if args.lookup_url:
        result = sbc.lookup(args.lookup_url)
        if result:
            pprint.pprint(result)
        sys.exit()

    # If no arguments were specifed, print the client config and service status
    print("No arguments specified. Printing client info and service status.\n")
    print(sbc)
    result = sbc.service_status()
    if result:
        print('GGLSBL Service status:')
        pprint.pprint(result)
    else:
        logger.warn("Service seems down. Got response: {}".format(sbc.last_response.text))

