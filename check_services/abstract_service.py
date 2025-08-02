# Author: Abyss93

from abc import ABC, abstractmethod


class AbstractService(ABC):

    @abstractmethod
    def process_ip(self, ip):
        pass

    @abstractmethod
    def process_domain(self, domain):
        pass
