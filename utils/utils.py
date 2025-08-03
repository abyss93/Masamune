# Author: Abyss93

import hashlib
import re


class Utils:
    CLASS_NAME = "Utils"

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def hashes_of(obj):
        md5 = hashlib.md5(obj).hexdigest()
        sha1 = hashlib.sha1(obj).hexdigest()
        sha256 = hashlib.sha256(obj).hexdigest()
        return {"md5": md5, "sha1": sha1, "sha256": sha256}

    @staticmethod
    def find_urls_and_domains(payload_type, payload):
        domains = []
        urls_res = []
        if payload_type == "html":
            urls = re.findall("(?<=href=\")(.*?)(?=\")", payload)
        else:
            urls = re.findall(
                r"(http:\/\/|https:\/\/|ftp:\/\/|www.\.?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,256}\b[-a-zA-Z0-9()@:%_\+.~#?&//=]*)",
                payload)

        filter_out = {"http://", "https://", "ftp://"}
        urls = [u for u in urls if u not in filter_out]
        if urls is not None and len(urls) > 0:
            for u in urls:
                urls_res.append(u.replace(".", "[.]").replace(":", "[:]"))
                domains.append(Utils.extract_domain_from_(u))

        urls_res = list(dict.fromkeys(urls_res))
        domains = list(dict.fromkeys(domains))
        # print("***** START URLs *****")
        # for r in urls_res:
        #    print(r)
        # print("***** END URLs *****")
        # print("***** DOMAINs *****")
        # for r in domains:
        #    print(r.replace(".", "[.]"))
        # print("***** END DOMAINs *****")
        return urls_res, domains

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
        if "Received" == header_name:
            # in Received headers, IPs are usually enclosed in square parentheses so I adapt the regex to avoid matching numbers that are not IP addresses
            pattern = "(?!\[)" + pattern + "(?=\])"
        return re.findall(pattern, header_value)

    @staticmethod
    def extract_domain_from_(url):
        # Thanks to https://medium.com/@glee8804/extracting-domains-from-urls-in-python-fa2bf0d01ac3
        # Define a regular expression pattern for extracting the domain
        pattern = r"(https?://)?(www\d?\.)?(?P<domain>[\w\.-]+\.\w+)(/\S*)?"
        # Use re.match to search for the pattern at the beginning of the URL
        match = re.match(pattern, url)
        # Check if a match is found
        if match:
            # Extract the domain from the named group "domain"
            domain = match.group("domain")
            return domain
        else:
            return ""

    # given an FQDN like abcd.efg.xyz.hi it returns
    # ["abcd.efg.xyz.hi", "xyz.hi"]
    # that is a list composed by [FQDN, SLD_dot_TLD]
    # these two are sufficient to have a meaningful check
    @staticmethod
    def get_fqdn_and_sld_from(domain: str):
        # domain = an FQDN
        res = [domain]
        arr = domain.split(".")
        if len(arr) > 2:
            sld_tld = arr[-2] + "." + arr[-1]
            res.append(sld_tld)
        return res

    @staticmethod
    def get_charset_from_content_type_header(content_type):
        # https://www.w3.org/Protocols/rfc1341/7_1_Text.html
        pattern = "charset=(ISO-8859-[0-9]{1,2}|utf-8|US-ASCII){1}"
        matches = re.findall(pattern, content_type, re.IGNORECASE)
        if matches:
            return matches[0]
        else:
            return None