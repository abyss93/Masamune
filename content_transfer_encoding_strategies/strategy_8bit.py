from content_transfer_encoding_strategies.abstract_strategy import AbstractStrategy


class Strategy8bit(AbstractStrategy):
    CLASS_NAME = "Strategy8bit"

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    def process(self, content_type, payload):
        # Unencoded 8-bit ASCII
        self.logger.log("Unencoded 8-bit ASCII | Content-Type: " + str(content_type), Strategy8bit.CLASS_NAME)

        if self.config["print_payload"]:
            print(f"***** RAW PAYLOAD {Strategy8bit.CLASS_NAME} *****")
            print(payload + "\n")

        if self.config["payload_analysis"]:
            print(f"***** PAYLOAD ANALYSIS {Strategy8bit.CLASS_NAME} *****")
            # TODO
            print("8bit")
            print("***** END ANALYSIS *****")
