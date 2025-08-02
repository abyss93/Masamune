# Author: Abyss93

import yaml


class ConfigParser:
    CLASS_NAME = "ConfigParser"

    def __init__(self, logger):
        self.logger = logger

    def parse(self, config_file_path):
        self.logger.log(f"Parsing {config_file_path}", self.CLASS_NAME)
        with open(config_file_path, 'r') as stream:
            config = yaml.safe_load(stream)
        self.logger.log(f"{config_file_path} parsed", self.CLASS_NAME)
        # this is a dict
        return config
