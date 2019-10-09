#!/usr/bin/env python3

import logging
import requests

from urllib.parse import urlparse

TEST_URL = 'http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/SOCIAL_ENGINEERING/URL/'

class GGLSBL_Rest_Service_Client():
    """A client to query the [gglsbl-rest](https://github.com/mlsecproject/gglsbl-rest) service.
    """
    logger = logging.getLogger(__name__+".GGLSBL_Rest_Service_Client")

    def __init__(self, hostname=None, port=None, ssl=False, timeout=10):
        self.server = hostname
        self.port = port
        self.ssl = ssl
        self.timeout = timeout
        self.lookup_url = None
        self.status_url = None
        if self.server is not None:
            if not self.ssl and not self.server.startswith('http://'):
                self.server = 'http://'+self.server+':'+self.port
            elif self.ssl and not self.server.startswith('https://'):
                self.server = 'https://'+self.server+':'+self.port
            self.lookup_url = self.server+'/gglsbl/lookup/'
            self.status_url = self.server+'/gglsbl/status'
        self.logger.debug("Lookup URL: '{}' && Status URL: '{}'".format(self.lookup_url, self.status_url))
        # store the last response for reference
        self._r = None

    @property
    def last_response(self):
        """Return the last response we got from the server.
        """
        return self._r

    def _query(self, query):
        try:
            self._r = requests.get(query, verify=self.ssl, timeout=self.timeout)
            return self._r
        except requests.exceptions.ReadTimeout as e:
            self.logger.error("ReadTimeout : gglsbl-rest server took longer than {} seconds to respond.".format(self.timeout))
            return False
        except Exception as e:
            self.logger.error("Problem connecting to service: {}".format(e))
            raise e

    def _encode_url(self, url):
        encoded_url = "".join('%%%02x' % ord(c) for c in url)
        self.logger.debug('Encoding URL: {} -> {}'.format(url, encoded_url))
        return encoded_url

    def _is_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])#, result.path])
        except:
            return False

    def lookup(self, url):
        """Lookup this url with the gglsbl-rest service
        """
        if not self._is_url(url):
            self.logger.warn("Provided URL does not appear valid: {}".format(url))
        self.logger.debug("Looking up '{}'".format(url))
        r = self._query(self.lookup_url+self._encode_url(url))
        if not r:
            # ReadTimeout occured
            return False
        self.logger.debug("Got {} response status code from server".format(r.status_code))
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            try:
                return r.json()
            except Exception as e:
                return r.text
        else:
            self.logger.error("Unexpected result from server: {} - {}".format(r.status_code, r.text))
            return False

    def service_status(self):
        """Get the status of the gglsbl-rest service.
        """
        r = self._query(self.status_url)
        self.logger.debug("Got {} response status code from server".format(r.status_code))
        if r.status_code == 200:
            return r.json()
        else:
            self.logger.error("Unexpected result from server: {} - {}".format(r.status_code, r.text))
            return False

    def __str__(self):
        txt = "GGLSBL_Rest_Service_Client\n"
        txt += "\tLookup URL: {}\n".format(self.lookup_url)
        txt += "\tStatus URL: {}\n".format(self.status_url)
        txt += "\n"
        return txt
