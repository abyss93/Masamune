# Author: Abyss93

import json

import requests

from check_services.abstract_service import AbstractService


class AlienVaultOTXService(AbstractService):
    CLASS_NAME = "AlienVaultOTXService"

    def __init__(self, logger, api_key):
        self.logger = logger
        self.api_key = api_key

    def process_ip(self, ip):
        headers = {
            'X-OTX-API-KEY': self.api_key
        }
        try:
            response = requests.get("https://otx.alienvault.com/api/v1/indicators/IPv4/" + ip + "/general",
                                    headers=headers)
            alienvaultotx = json.loads(response.text)
            self.logger.log("-----> ALIENVAULT")
            self.logger.log("- ASN: " + str(alienvaultotx["asn"]))
            self.logger.log("- Validation: " + str(alienvaultotx["validation"]))
            self.logger.log("- Pulse info")
            self.logger.log("     |- Pulse count: " + str(alienvaultotx["pulse_info"]["count"]))
            pulses = alienvaultotx["pulse_info"]["pulses"]
            for i, p in enumerate(pulses):
                # sanitization of Name, I don't want to risk clicking some malicious link that could have been included in the name field
                self.logger.log(
                    f'     |- Pulse {i} -> Name: {p["name"].replace(":", "[:]").replace(".", "[.]")} | Tags: {p["tags"]} | ModDate: {p["modified"]} | MlwFam: {p["malware_families"]}')
            # self.logger.log("     |- References: " + str(alienvaultotx["pulse_info"]["references"]))
            self.logger.log("     |- Related, AlienVault")
            self.logger.log(
                "          |- Adversary: " + str(alienvaultotx["pulse_info"]["related"]["alienvault"]["adversary"]))
            self.logger.log("          |- Malware families: " + str(
                alienvaultotx["pulse_info"]["related"]["alienvault"]["malware_families"]))
            self.logger.log(
                "          |- Industries: " + str(alienvaultotx["pulse_info"]["related"]["alienvault"]["industries"]))
            self.logger.log("     |- Related, Others")
            self.logger.log(
                "          |- Adversary: " + str(alienvaultotx["pulse_info"]["related"]["other"]["adversary"]))
            self.logger.log("          |- Malware families: " + str(
                alienvaultotx["pulse_info"]["related"]["other"]["malware_families"]))
            self.logger.log(
                "          |- Industries: " + str(alienvaultotx["pulse_info"]["related"]["other"]["industries"]))
            alienvaultotx = {
                "indicator": alienvaultotx["indicator"],
                "type": alienvaultotx["type"],
                "country_code": alienvaultotx["country_code"],
                "reputation": alienvaultotx["reputation"],
                "pulses_count": alienvaultotx["pulse_info"]["count"]
            }
        except:
            alienvaultotx = {
                "Error": f"Status code: {response.status_code} \nReason: {response.reason} \n{response.text}"}
        return {"service_name": self.CLASS_NAME, "IP": ip, "processing_result": alienvaultotx}

    def process_domain(self, domain):
        domain_safe = domain.replace('.', '[.]')
        self.logger.log(f"Checking domain {domain_safe}", AlienVaultOTXService.CLASS_NAME)
        headers = {
            'X-OTX-API-KEY': self.api_key
        }
        try:
            response = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general",
                                    headers=headers)

            alienvaultotx = json.loads(response.text)
            self.logger.log("-----> ALIENVAULT")
            self.logger.log("- Pulse info")
            self.logger.log("     |- Pulse count: " + str(alienvaultotx["pulse_info"]["count"]))
            response = requests.get(f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general",
                                    headers=headers)
            alienvaultotx = json.loads(response.text)
            alienvaultotx = {
                "pulses_count": alienvaultotx["pulse_info"]["count"]
            }
        except:
            alienvaultotx = {
                "Error": f"Status code: {response.status_code} \nReason: {response.reason} \n{response.text}"}
        return {"service_name": self.CLASS_NAME, "domain": domain_safe, "processing_result": alienvaultotx}
