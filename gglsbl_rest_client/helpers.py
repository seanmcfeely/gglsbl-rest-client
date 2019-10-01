import os
import logging
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(profile='default', required_options=[]):
    """Load GGLSBL-Rest configuration. Configuration files are looked for in the following locations::
        /<python-lib-where-installed>/etc/config.ini
        /etc/gglsbl-rest/config.ini
        ~/<current-user>/.config/gglsbl-rest.ini

    Configuration items found in later config files take presendence over earlier ones.

    :param str profile: (optional) Specifiy a group or company to work with.
    """
    logger = logging.getLogger(__name__+".load_config")
    config = ConfigParser()
    config_paths = []
    # default
    config_paths.append(os.path.join(BASE_DIR, 'etc', 'config.ini'))
    # global
    config_paths.append('/etc/gglsbl-rest/config.ini')
    # user specific
    config_paths.append(os.path.join(os.path.expanduser("~"),'.config','gglsbl-rest.ini'))
    finds = []
    for cp in config_paths:
        if os.path.exists(cp):
            logger.debug("Found config file at {}.".format(cp))
            finds.append(cp)
    if not finds:
        logger.critical("Didn't find any config files defined at these paths: {}".format(config_paths))
        return False

    config.read(finds)
    try:
        config[profile]
    except KeyError:
        logger.critical("No section named '{}' in configuration files : {}".format(profile, config_paths))
        return False

    for op in required_options:
        if not config.has_option(profile, op):
            logger.error("Configuation missing required options: {}".format(op))
            return False
        elif not config[profile][op]:
            logger.error("Configuration option missing value: {}".format(op))
            return False

    return config[profile]
