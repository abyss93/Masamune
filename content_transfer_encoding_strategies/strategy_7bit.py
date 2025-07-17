from content_transfer_encoding_strategies.abstract_strategy import AbstractStrategy


class Strategy7bit(AbstractStrategy):
    CLASS_NAME = "Strategy7bit"

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    def process(self, content_type, payload):
        self.logger.log("Unencoded 7-bit ASCII | Content-Type: " + str(content_type), Strategy7bit.CLASS_NAME)

        if self.config["print_payload"]:
            print(f"***** RAW PAYLOAD {Strategy7bit.CLASS_NAME} *****")
            print(payload + "\n")

        if self.config["payload_analysis"]:
            print(f"***** PAYLOAD ANALYSIS {Strategy7bit.CLASS_NAME} *****")
            body = ''.join(payload)
            print(body)
            if "text/plain" in content_type:
                res_print, res_domains = self.utils.find_urls("text/plain", body)
            elif "text/html" in content_type:
                res_print, res_domains = self.utils.find_urls("html", body)
            if res_domains:
                matches = []
                for d in res_domains:
                    matches = matches + self.services["feed_service"].process_domain(d)
            print("***** END ANALYSIS *****")
