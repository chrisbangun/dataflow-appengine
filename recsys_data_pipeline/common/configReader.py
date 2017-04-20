#!/usr/bin/env python

import os
import yaml


class ConfigReader(object):

    configuration = None

    def __init__(self, config_name):
        self.config_name = config_name
        self.configuration = self.__get_config_data(config_name)


    def __get_config_data(self, config_name):
        """
        :param config_name: configuration name define in the config file
        :return: dict
        """
        config_path = self.path_from_here('../config/config.yaml')
        with open(config_path) as f:
            config_file = yaml.load(f)
        return config_file[config_name]

    def path_from_here(self, path):
        return os.path.join(os.path.dirname(__file__), path)