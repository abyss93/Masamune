from content_transfer_encoding_strategies.abstract_strategy import AbstractStrategy


class StrategyFallback(AbstractStrategy):
    CLASS_NAME = "StrategyFallback"

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    def process(self, content_type, payload):
        # Encoded 7-bit ASCII
        self.logger.log("Fallback strategy | Content-Type: " + str(content_type), StrategyFallback.CLASS_NAME)
        if self.config["print_payload"]:
            print(f"***** RAW PAYLOAD {StrategyFallback.CLASS_NAME} *****")
            print(payload + "\n")

        if self.config["payload_analysis"]:
            print(f"***** PAYLOAD ANALYSIS {StrategyFallback.CLASS_NAME} *****")
            if self.config["debug"]: self.logger.log(payload)
            res_print, res_domains = self.utils.find_urls("fallback", payload)
            if res_domains:
                matches = []
                for d in res_domains:
                    matches = matches + self.services["feed_service"].process_domain(d)
            # TODO
            print("***** END ANALYSIS *****")
