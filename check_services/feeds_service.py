# Author: Abyss93

import os
from datetime import datetime

import requests

from check_services.abstract_service import AbstractService
from feeds import FEEDS


class FeedService(AbstractService):
    CLASS_NAME = "FeedsService"

    def __init__(self, logger, feed_folder_path):
        self.logger = logger
        self.feed_folder = feed_folder_path

    def download(self, url, path):
        self.logger.log(f"Downloading {url}", FeedService.CLASS_NAME)
        r = requests.get(url)
        with open(path, 'w') as feed_file:
            self.logger.log(f"Writing {path}", FeedService.CLASS_NAME)
            feed_file.write(bytes.decode(r.content))

    def update(self):
        for feed in FEEDS:
            url = feed["url"]
            update_interval_minutes = feed["update_interval_minutes"]
            path = self.feed_folder + feed["filename"]
            if os.path.exists(path):
                self.logger.log(f"Feed '{feed['name']}' file exists", FeedService.CLASS_NAME)
                modify_time = os.path.getmtime(path)
                modify_date = datetime.fromtimestamp(modify_time)
                minutes_diff = (datetime.today() - modify_date).total_seconds() / 60.0
                if minutes_diff >= update_interval_minutes:
                    self.logger.log(f"Feed '{feed['name']}' outdated UPDATING", FeedService.CLASS_NAME)
                    self.download(url, path)
            else:
                self.logger.log(f"Feed '{feed['name']}' file does not exists", FeedService.CLASS_NAME)
                self.download(url, path)

    def process_domain(self, domain):
        matches = []
        domain_safe = domain.replace('.', '[.]')
        self.logger.log(f"Checking domain {domain_safe}", FeedService.CLASS_NAME)
        for f in FEEDS:
            self.logger.log("-----> " + f["name"])
            if f["check_what"] == "domain":
                feed_path = self.feed_folder + f["filename"]
                with open(feed_path, 'r') as feed_file:
                    self.logger.log(f"Reading {feed_path}", FeedService.CLASS_NAME)
                    found = False
                    for line in feed_file:
                        if domain in line:
                            self.logger.log(f"Match found on feed {f['name']}", FeedService.CLASS_NAME)
                            matches.append((f["name"], domain_safe))
                            found = True
                            break
                    if not found:
                        self.logger.log("not found in feed " + f["name"])
        return {"service_name": self.CLASS_NAME, "domain": domain_safe, "processing_result": {"Matches": matches}}

    # TODO eventually add a method to check IP
    def process_ip(self, ip):
        return {"service_name": self.CLASS_NAME, "IP": ip,
                "processing_result": {"Error": "this service cannot process IPs"}}
