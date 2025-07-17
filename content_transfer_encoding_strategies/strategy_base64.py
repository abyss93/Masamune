import base64

from content_transfer_encoding_strategies.abstract_strategy import AbstractStrategy


class StrategyBase64(AbstractStrategy):
    CLASS_NAME = "StrategyBase64"

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    def process(self, content_type, payload):
        self.logger.log("BASE64 | Content-Type: " + str(content_type), StrategyBase64.CLASS_NAME)

        if self.config["print_payload"]:
            print(f"***** RAW PAYLOAD {StrategyBase64.CLASS_NAME} *****")
            print(payload + "\n")

        if self.config["payload_analysis"]:
            print(f"***** PAYLOAD ANALYSIS {StrategyBase64.CLASS_NAME} *****")
            body = ''.join(payload).replace("\n", "")
            decoded = base64.b64decode(body)
            if self.config["debug"]: self.logger.log(body)
            self.utils.hashes_of(decoded)
            # print(decoded)
            # if self.config["find_urls"]: self.utils.find_urls(decoded)
            # TODO
            print("***** END ANALYSIS *****")
