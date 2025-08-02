# Author: Abyss93

from payload_analysis.abstract_strategy import AbstractStrategy
from payload_analysis.strategy_result import StrategyResult


class StrategyFallback(AbstractStrategy):
    CLASS_NAME = "StrategyFallback"

    def __init__(self, config, logger, utils, services):
        super().__init__(config, logger, utils, services)

    def process(self, content_type, payload):
        result = StrategyResult()
        result.payload_to_print = payload
        # Encoded 7-bit ASCII
        self.logger.log("Fallback strategy | Content-Type: " + str(content_type), StrategyFallback.CLASS_NAME)
        self.logger.log(f"***** RAW PAYLOAD {StrategyFallback.CLASS_NAME} *****", StrategyFallback.CLASS_NAME)
        self.logger.log(payload + "\n", StrategyFallback.CLASS_NAME)

        if self.config["payload_analysis"]:
            self.logger.log(f"***** PAYLOAD ANALYSIS {StrategyFallback.CLASS_NAME} *****", StrategyFallback.CLASS_NAME)
            self.logger.log(payload, StrategyFallback.CLASS_NAME)
            urls, domains = self.utils.find_urls_and_domains("fallback", payload)
            matches = []
            if domains:
                for d in domains:
                    matches.extend(self.process_domain(d))
                self.logger.log(f"Matches: {matches}", StrategyFallback.CLASS_NAME)
            result.domain_feed_matches = matches
            result.urls = urls
            result.domains = domains
            self.logger.log("***** END ANALYSIS *****", StrategyFallback.CLASS_NAME)
        return result
