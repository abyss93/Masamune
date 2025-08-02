# Author: Abyss93

from header_analysis.header_analyzer_result import HeaderAnalyzerResult


class HeaderAnalyzer:
    CLASS_NAME = "HeaderAnalyzer"

    def __init__(self, logger, utils, services, email_address_whitelist, domains_whitelist):
        self.logger = logger
        self.utils = utils
        self.services = services
        self.domains_whitelist = domains_whitelist
        self.email_address_whitelist = email_address_whitelist

    def analyze(self, headers):
        # "headers" is a list of tuple, each tuple consist of the name of the header (index 0) and its value (index 1)
        result = HeaderAnalyzerResult()
        # dictionaries where key is the header name and value is an array of found elements
        email_addresses = []
        domains = []
        ips = []

        for header in headers:
            header_name = header[0]
            header_value = header[1]
            if header_name == "Message-ID":
                continue
            # HEADERS
            # TODO analyze spf, dmarc, dkim, etc???
            # EMAIL ADDRESSES
            found_email_addresses = self.utils.look_for_email_addresses(header_value)
            email_addresses.append((header_name, found_email_addresses))
            # DOMAINS
            domains.append((header_name, self.utils.look_for_email_addresses_domains(found_email_addresses)))
            # IPs
            ips.append((header_name, self.utils.look_for_ip_address(header_name, header_value)))

        # prepare result
        result.email_addresses = email_addresses
        result.domain = domains
        result.ips = ips

        self.logger.log("\n****** FOUND_EMAIL_ADDRESSES ******", self.CLASS_NAME)
        email_addresses_to_analyze_no_duplicates = []

        for h_ea in email_addresses:
            if isinstance(h_ea[1], list) and len(h_ea[1]) > 0:
                self.logger.log(f"{h_ea[0]} -> {'; '.join(set(h_ea[1]))}", self.CLASS_NAME)
                for ea in h_ea[1]:
                    ea_temp = str(ea)
                    ea_temp = ea_temp.replace("smtp.mailfrom=", "")
                    if ea not in email_addresses_to_analyze_no_duplicates and "smtp.mailfrom=" not in ea:
                        email_addresses_to_analyze_no_duplicates.append(ea)
                    if not ea_temp in email_addresses_to_analyze_no_duplicates:
                        email_addresses_to_analyze_no_duplicates.append(ea_temp)

        # TODO check if email address is a known phishing sender, need to find an appropriate feed for that
        # for ea in email_addresses_to_analyze_no_duplicates:
        #     if ea not in self.email_address_whitelist:
        #         self.logger.log(f"ANALYSIS {ea}", self.CLASS_NAME)
        self.logger.log("***********************************", self.CLASS_NAME)

        self.logger.log("\n********** FOUND_DOMAINS **********", self.CLASS_NAME)
        domains_to_analyze_no_duplicates = []

        for h_d in domains:
            if isinstance(h_d[1], list) and len(h_d[1]) > 0:
                self.logger.log(f"{h_d[0]} -> {'; '.join(set(h_d[1]))}", self.CLASS_NAME)
                for d in h_d[1]:
                    if d not in domains_to_analyze_no_duplicates:
                        domains_to_analyze_no_duplicates.append(d)

        for d in domains_to_analyze_no_duplicates:
            if d not in self.domains_whitelist:
                self.logger.log(f"ANALYSIS {d}", self.CLASS_NAME)
                alienvault_matches = self.services['alienvault_otx'].process_domain(d)
                feed_service_matches = self.services['feed_service'].process_domain(d)
                result.add_domain_result(alienvault_matches)
                result.add_domain_result(feed_service_matches)
                self.logger.log(f"Matches: {alienvault_matches}", self.CLASS_NAME)
                self.logger.log(f"Matches: {feed_service_matches}", self.CLASS_NAME)
            else:
                self.logger.log(f"-----> Skipping whitelisted domain: {d}")
        self.logger.log("***********************************", self.CLASS_NAME)

        self.logger.log("\n********** FOUND_IPs **************", self.CLASS_NAME)
        ips_to_analyze_no_duplicates = []

        for h_ip in ips:
            if isinstance(h_ip[1], list) and len(h_ip[1]) > 0:
                self.logger.log(f"{h_ip[0]} -> {'; '.join(set(h_ip[1]))}", self.CLASS_NAME)
                for ip in h_ip[1]:
                    if ip not in ips_to_analyze_no_duplicates:
                        ips_to_analyze_no_duplicates.append(ip)

        for ip in ips_to_analyze_no_duplicates:
            self.logger.log(f"ANALYSIS {ip}", self.CLASS_NAME)
            abuseipdb_matches = self.services['abuseipdb'].process_ip(ip)
            alienvault_ip_matches = self.services['alienvault_otx'].process_ip(ip)
            result.add_ip_result(abuseipdb_matches)
            result.add_ip_result(alienvault_ip_matches)
            self.logger.log(f"Matches: {abuseipdb_matches}", self.CLASS_NAME)
            self.logger.log(f"Matches: {alienvault_ip_matches}", self.CLASS_NAME)
        self.logger.log("***********************************", self.CLASS_NAME)

        return result
