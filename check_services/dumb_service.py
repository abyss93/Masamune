from check_services.abstract_service import AbstractService


class DumbService(AbstractService):
    CLASS_NAME = "DumbService"

    def __init__(self, logger, replacement_of):
        self.replacement_of = replacement_of
        self.logger = logger

    def process_ip(self, ip):
        self.logger.log(f"{self.replacement_of} API KEY is not configured, cannot process {ip}", self.CLASS_NAME)

    def process_domain(self, domain):
        self.logger.log(f"{self.replacement_of} API KEY is not configured, cannot process {domain}", self.CLASS_NAME)
