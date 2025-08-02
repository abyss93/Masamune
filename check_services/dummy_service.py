# Author: Abyss93

from check_services.abstract_service import AbstractService


class DummyService(AbstractService):
    CLASS_NAME = "DummyService"

    def __init__(self, logger, replacement_of):
        self.replacement_of = replacement_of
        self.logger = logger

    def process_ip(self, ip):
        self.logger.log(f"-----> {self.replacement_of} API KEY is not configured, cannot process", self.CLASS_NAME)
        return {"service_name": self.CLASS_NAME, "IP": ip,
                "processing_result": {"Error": "API KEY is not configured, cannot process"}}

    def process_domain(self, domain):
        self.logger.log(f"-----> {self.replacement_of} API KEY is not configured, cannot process", self.CLASS_NAME)
        domain_safe = domain.replace('.', '[.]')
        return {"service_name": self.CLASS_NAME, "domain": domain_safe,
                "processing_result": {"Error": "API KEY is not configured, cannot process"}}
