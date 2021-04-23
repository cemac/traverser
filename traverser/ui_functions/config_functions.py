# -*- coding: utf-8 -*-
"""
Configuration functions
"""

# Standard lib imports:
from configparser import ConfigParser
import os
# Package imports:
from traverser.functions import convert_numeric
from traverser.config import Config

def read_config(config, config_file):
    """
    Try to read config values from file
    """
    # Try to open the file:
    try:
        config_fh = open(config_file, 'r')
    except:
        return False, config
    config_fh.close()
    # Use config parser to read the file:
    parser = ConfigParser()
    parser.read(config_file)
    # Get traverser values:
    try:
        parsed = parser['traverser']
    except KeyError:
        return False, config
    # Loop through expected config values:
    for config_value in config.config_values:
        # If value exists, add to config:
        try:
            config.values[config_value] = convert_numeric(
                parsed[config_value]
            )
        except KeyError:
            pass
    # Return the updated config:
    return True, config

def write_config(ui, config, config_file=None):
    """
    Save current config to file
    """
    # If no file specified, use default location:
    if not config_file:
        config_file = config.default_config
    # Use config parser to write the config file:
    parser = ConfigParser()
    parser['traverser'] = config.values
    # Try to write the config file:
    try:
        with open(config_file, 'w') as config_fh:
            parser.write(config_fh)
        err_msg = 'Config saved to {0}'.format(config_file)
        status = True
    except:
        err_msg = 'Failed to write config_file {0}'.format(config_file)
        status = False
    # Log a message:
    ui.log_message(err_msg, status)

def get_config(ui):
    """
    Get the inital Traverser configuration
    """
    # Init config:
    config = Config()
    # Check if default config file exists:
    if os.path.exists(config.default_config):
        # Try to load config values:
        status, config = read_config(config, config.default_config)
    # Save the config:
    write_config(ui, config)
    # Return the config:
    return config
