from content_transfer_encoding_strategies.abstract_strategy import AbstractStrategy


class StrategyBinary(AbstractStrategy):
    CLASS_NAME = "StrategyBinary"

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    def process(self, content_type, payload):
        # Unencoded 8-bit ASCII
        self.logger.log("Binary | Content-Type: " + str(content_type), StrategyBinary.CLASS_NAME)

        if self.config["print_payload"]:
            print(f"***** RAW PAYLOAD {StrategyBinary.CLASS_NAME} *****")
            print(payload + "\n")

        if self.config["payload_analysis"]:
            print(f"***** PAYLOAD ANALYSIS {StrategyBinary.CLASS_NAME} *****")
            # TODO
            self.utils.hashes_of(payload)
            print("***** END ANALYSIS *****")
