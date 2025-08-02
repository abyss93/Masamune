# Author: Abyss93

from abc import ABC, abstractmethod


class AbstractStrategy(ABC):

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    @abstractmethod
    def process(self, content_type, payload):
        pass

    def process_domain(self, domain):
        matches = []
        self.logger.log(f"ANALYSIS {domain.replace('.', '[.]')}")
        domains_to_check = self.utils.get_fqdn_and_sld_from(domain)
        for d in domains_to_check:
            matches.append(self.services["feed_service"].process_domain(d))
            matches.append(self.services["alienvault_otx"].process_domain(d))
        return matches
