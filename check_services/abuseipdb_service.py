# Author: Abyss93

import json

import requests

from check_services.abstract_service import AbstractService


class AbuseipDBService(AbstractService):
    CLASS_NAME = "AbuseipDBService"

    def __init__(self, logger, api_key):
        self.api_key = api_key
        self.logger = logger

    def process_ip(self, ip):
        headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }
        params = {
            'ipAddress': ip,
            'maxAgeInDays': '90',
        }
        try:
            self.logger.log(f"Processing {ip}, calling https[:]//api[.]abuseipdb[.]com/api/v2/check", self.CLASS_NAME)
            response = requests.get('https://api.abuseipdb.com/api/v2/check', params=params, headers=headers)
            abuseipdb_info = json.loads(response.text)
            abuseipdb_info_data = abuseipdb_info["data"]
            self.logger.log("-----> ABUSEIPDB")
            self.logger.log("- Country: " + str(abuseipdb_info_data["countryCode"]))
            self.logger.log("- Usage type: " + str(abuseipdb_info_data["usageType"]))
            self.logger.log("- ISP: " + str(abuseipdb_info_data["isp"]))
            self.logger.log("- Domain: " + str(abuseipdb_info_data["domain"]))
            self.logger.log("- Hostnames: " + str(abuseipdb_info_data["hostnames"]))
            self.logger.log("- Number of reports: " + str(abuseipdb_info_data["totalReports"]))
            self.logger.log("- Last reported at: " + str(abuseipdb_info_data["lastReportedAt"]))
            self.logger.log("- IsTor (bool): " + str(abuseipdb_info_data["isTor"]))
            abuseipdb_info_data = {
                "ipAddress": abuseipdb_info_data["ipAddress"],
                "isPublic": abuseipdb_info_data["isPublic"],
                "isWhitelisted": abuseipdb_info_data["isWhitelisted"],
                "usageType": abuseipdb_info_data["usageType"],
                "isp": abuseipdb_info_data["isp"],
                "isTor": abuseipdb_info_data["isTor"],
                "totalReports": abuseipdb_info_data["totalReports"],
                "numDistinctUsers": abuseipdb_info_data["numDistinctUsers"],
                "lastReportedAt": abuseipdb_info_data["lastReportedAt"]
            }
        except:
            abuseipdb_info_data = f"Status code: {response.status_code} \nReason: {response.reason} \n{response.text}"
        return {"service_name": self.CLASS_NAME, "IP": ip, "processing_result": abuseipdb_info_data}

    def process_domain(self, domain):
        self.logger.log(f"{self.CLASS_NAME} is unable to process domain names")
        domain_safe = domain.replace('.', '[.]')
        return {"service_name": self.CLASS_NAME, "domain": domain_safe,
                "processing_result": {"Error": "this service cannot process domains"}}


class AbuseipDBInfo:

    def __init__(self, abuseipdb_info):
        self.abuseipdb_info = abuseipdb_info

    def __str__(self):
        return
