import requests
import json

from check_services.abstract_service import AbstractService


class AbuseipDBService(AbstractService):
    
    CLASS_NAME = "AbuseipDBService"
    
    def __init__(self, logger, api_key):
        self.api_key = api_key
        self.logger = logger

    def process_ip(self, ip):
        print(f"\nANALYSIS {ip}")
        headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }
        params = {
            'ipAddress': ip,
            'maxAgeInDays': '90',
        }
        self.logger.log(f"Processing {ip}, calling https[:]//api[.]abuseipdb[.]com/api/v2/check", self.CLASS_NAME)
        response = requests.get('https://api.abuseipdb.com/api/v2/check', params=params, headers=headers)
        abuseipdb_info = json.loads(response.text)
        abuseipdb_info_data = abuseipdb_info["data"]
        print("-----> ABUSEIPDB")
        print("- Country: " + str(abuseipdb_info_data["countryCode"]))
        print("- Usage type: " + str(abuseipdb_info_data["usageType"]))
        print("- ISP: " + str(abuseipdb_info_data["isp"]))
        print("- Domain: " + str(abuseipdb_info_data["domain"]))
        print("- Hostnames: " + str(abuseipdb_info_data["hostnames"]))
        print("- Number of reports: " + str(abuseipdb_info_data["totalReports"]))
        print("- Last reported at: " + str(abuseipdb_info_data["lastReportedAt"]))
        print("- IsTor (bool): " + str(abuseipdb_info_data["isTor"]))
        return
    
    def process_domain(self, domain):
        print(f"{self.CLASS_NAME} is unable to process domain names")