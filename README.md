# python client for gglsbl-rest service

This is a simple python client wrapper for the [gglsbl-rest](https://github.com/mlsecproject/gglsbl-rest) service.

## Installation

``pip install gglsbl-rest-client``

## The gglsbl-rest-client CLI script

When installed, a commannd line script named 'gglsbl-rest-client' is supplied that can be used to query your [gglsbl-rest](https://github.com/mlsecproject/gglsbl-rest) service.
The default configuration file assumes you have the service running on local host. If you do not, the script checks the following locations for config files and overrides previous entries:

- ``/<local-dir>/etc/config.ini``
- ``/etc/gglsbl-rest/config.ini``
- ``~/<current-user>/.config/gglsbl-rest.ini``

```bash
$ gglsbl-rest-client.py -h
usage: gglsbl-rest-client.py [-h] [-d] [-rh REMOTE_HOST] [-p PORT] [-cs]
                             [-l LOOKUP_URL] [--ignore-proxy]

A client for querying MLSec gglsbl-rest Services
(https://github.com/mlsecproject)

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           set logging to DEBUG
  -rh REMOTE_HOST, --remote-host REMOTE_HOST
                        the hostname or IP address where the service is
                        listening. Default is localhost.
  -p PORT, --port PORT  the port the service is listening on. Default: 5000
  -cs, --check-status   Check the status of the service
  -l LOOKUP_URL, --lookup-url LOOKUP_URL
                        the url to lookup
  --ignore-proxy        ignore system proxy. On by default.
```

## Examples

### URL Lookup

```bash
$ gglsbl-rest-client.py -l 'http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/SOCIAL_ENGINEERING/URL/'
{'matches': [{'platform': 'ANY_PLATFORM',
              'threat': 'SOCIAL_ENGINEERING',
              'threat_entry': 'URL'},
             {'platform': 'WINDOWS',
              'threat': 'SOCIAL_ENGINEERING',
              'threat_entry': 'URL'},
             {'platform': 'LINUX',
              'threat': 'SOCIAL_ENGINEERING',
              'threat_entry': 'URL'},
             {'platform': 'OSX',
              'threat': 'SOCIAL_ENGINEERING',
              'threat_entry': 'URL'},
             {'platform': 'ALL_PLATFORMS',
              'threat': 'SOCIAL_ENGINEERING',
              'threat_entry': 'URL'},
             {'platform': 'CHROME',
              'threat': 'SOCIAL_ENGINEERING',
              'threat_entry': 'URL'}],
 'url': 'http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/SOCIAL_ENGINEERING/URL/'}
```

### Status Check

```bash
$ gglsbl-rest-client.py -cs
{'alternatives': [{'active': True,
                   'ctime': '2019-10-01T18:15:44+0000',
                   'mtime': '2019-10-01T18:15:44+0000',
                   'name': '/home/gglsbl/db/sqlite.db',
                   'size': 1389404160}],
 'environment': 'prod'}
```

OR

```bash
$ gglsbl-rest-client.py 
No arguments specified. Printing client info and service status.

GGLSBL_Rest_Service_Client
	Lookup URL: http://127.0.0.1:5000/gglsbl/lookup/
	Status URL: http://127.0.0.1:5000/gglsbl/status


GGLSBL Service status:
{'alternatives': [{'active': True,
                   'ctime': '2019-10-01T18:15:44+0000',
                   'mtime': '2019-10-01T18:15:44+0000',
                   'name': '/home/gglsbl/db/sqlite.db',
                   'size': 1389404160}],
 'environment': 'prod'}
```
