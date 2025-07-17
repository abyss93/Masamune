import requests
import json

from check_services.abstract_service import AbstractService


class AlienVaultOTXService(AbstractService):
    
    CLASS_NAME = "AlienVaultOTXService"
    
    def __init__(self, logger, api_key):
        self.logger = logger
        self.api_key = api_key

    def process_ip(self, ip):
        print(f"\nANALYSIS {ip}")
        headers = {
            'X-OTX-API-KEY': self.api_key
        }
        response = requests.get("https://otx.alienvault.com/api/v1/indicators/IPv4/"+ ip + "/general", headers=headers)
        alienvaultotx = json.loads(response.text)
        print("-----> ALIENVAULT")
        print("- ASN: " + str(alienvaultotx["asn"]))
        print("- Validation: " + str(alienvaultotx["validation"]))
        print("- Pulse info")
        print("     |- Pulse count: " + str(alienvaultotx["pulse_info"]["count"]))
        pulses = alienvaultotx["pulse_info"]["pulses"]
        for i, p in enumerate(pulses):
            # sanitization of Name, I don't want to risk clicking some malicious link that could have been included in the name field
            print(f'     |- Pulse {i} -> Name: {p["name"].replace(":", "[:]").replace(".", "[.]")} | Tags: {p["tags"]} | ModDate: {p["modified"]} | MlwFam: {p["malware_families"]}')
        # print("     |- References: " + str(alienvaultotx["pulse_info"]["references"]))
        print("     |- Related, AlienVault")
        print("          |- Adversary: " + str(alienvaultotx["pulse_info"]["related"]["alienvault"]["adversary"]))
        print("          |- Malware families: " + str(alienvaultotx["pulse_info"]["related"]["alienvault"]["malware_families"]))
        print("          |- Industries: " + str(alienvaultotx["pulse_info"]["related"]["alienvault"]["industries"]))
        print("     |- Related, Others")
        print("          |- Adversary: " + str(alienvaultotx["pulse_info"]["related"]["other"]["adversary"]))
        print("          |- Malware families: " + str(alienvaultotx["pulse_info"]["related"]["other"]["malware_families"]))
        print("          |- Industries: " + str(alienvaultotx["pulse_info"]["related"]["other"]["industries"]))

    def process_domain(self, domain):
        domain_safe = domain.replace('.', '[.]')
        print(f"ANALYSIS {domain_safe}")
        self.logger.log(f"Checking domain {domain_safe}", AlienVaultOTXService.CLASS_NAME)
        headers = {
            'X-OTX-API-KEY': self.api_key
        }
        response = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general",
                                headers=headers)
        alienvaultotx = json.loads(response.text)
        print("-----> ALIENVAULT")
        print("- Pulse info")
        print("     |- Pulse count: " + str(alienvaultotx["pulse_info"]["count"]))
        response = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/malware",
                                headers=headers)
        alienvaultotx = json.loads(response.text)
        print("     |- Malware linked to domain: " + str(alienvaultotx["size"]))