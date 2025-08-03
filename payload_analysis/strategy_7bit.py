# Author: Abyss93

from payload_analysis.abstract_strategy import AbstractStrategy
from payload_analysis.strategy_result import StrategyResult


class Strategy7bit(AbstractStrategy):
    CLASS_NAME = "Strategy7bit"

    def __init__(self, config, logger, utils, services):
        super().__init__(config, logger, utils, services)

    def process(self, content_type, payload):
        result = StrategyResult()
        result.payload_to_print = payload
        self.logger.log("Unencoded 7-bit ASCII | Content-Type: " + str(content_type), Strategy7bit.CLASS_NAME)
        self.logger.log(f"***** RAW PAYLOAD {Strategy7bit.CLASS_NAME} *****")
        self.logger.log(payload + "\n")

        if self.config["payload_analysis"]:
            self.logger.log(f"***** PAYLOAD ANALYSIS {Strategy7bit.CLASS_NAME} *****")
            body = ''.join(payload)
            urls, domains = [], []
            if "text/plain" in content_type:
                urls, domains = self.utils.find_urls_and_domains("text/plain", body)
            elif "text/html" in content_type:
                urls, domains = self.utils.find_urls_and_domains("html", body)
            matches = []
            if domains:
                for d in domains:
                    matches.extend(self.process_domain(d))
            result.domains = domains
            result.urls = urls
            result.domain_feed_matches = matches
            self.logger.log("***** END ANALYSIS *****")
        return result
