import hashlib
import re
from urllib.parse import urlparse


class Utils:
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def hashes_of(obj):
        print("***** HASHES *****")
        # md5 = hashlib.md5(obj).hexdigest()
        # sha1 = hashlib.sha1(obj).hexdigest()
        sha256 = hashlib.sha256(obj).hexdigest()
        print(f"sha256sum: {sha256}")
        print(f"\t\_ PIVOT TO VT: https://www.virustotal.com/gui/search/{sha256}")
        print("***** END_HASHES *****")

    @staticmethod
    def find_urls(string_type, string_to_check):
        res_print = []
        res_domains = []
        if string_type == "html":
            urls = re.findall("(?<=href=\")(.*?)(?=\")", string_to_check)
        else:
            urls = re.findall(
                r"((http:\/\/|https:\/\/|ftp:\/\/|www.)\.?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
                string_to_check)

        if urls is not None and len(urls) > 0:
            for url in urls:
                res_print.append(url[0].replace(".", "[.]").replace(":", "[:]"))
                res_domains.append(Utils.extract_domain_from_(url[0]))

        res_print = list(dict.fromkeys(res_print))
        res_domains = list(dict.fromkeys(res_domains))
        print("***** START URLs *****")
        for r in res_print:
            print(r)
        print("***** END URLs *****")
        print("***** DOMAINs *****")
        for r in res_domains:
            print(r.replace(".", "[.]"))
        print("***** END DOMAINs *****")
        return res_print, res_domains

    @staticmethod
    def look_for_email_addresses(text):
        pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
        return re.findall(pattern, text)

    @staticmethod
    def look_for_email_addresses_domains(email_addresses):
        res = []
        for ea in email_addresses:
            res.append(ea.split("@")[1])
        return res

    @staticmethod
    def look_for_ip_address(header_name, header_value):
        pattern = "(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])"
        if "Received" in header_name:
            # in Received headers, IPs are usually enclosed in square parentheses so I adapt the regex to avoid matching numbers that are not IP addresses
            pattern = "(?!\[)" + pattern + "(?=\])"
        return re.findall(pattern, header_value)

    @staticmethod
    def extract_domain_from_(url):
        return urlparse(url).netloc.replace("www.", "")
