# Author: Abyss93

class HeaderAnalyzerResult:

    def __init__(self):
        self.ips = []
        self.ip_results = []
        self.domains = []
        self.domain_results = []
        self.email_addresses = []
        self.email_address_results = []

    def add_ip_result(self, ip_result):
        self.ip_results.append(ip_result)

    def add_domain_result(self, domain_result):
        self.domain_results.append(domain_result)

    def add_email_address_result(self, email_address_result):
        self.email_address_results.append(email_address_result)
