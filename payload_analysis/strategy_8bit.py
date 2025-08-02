# Author: Abyss93

from payload_analysis.abstract_strategy import AbstractStrategy
from payload_analysis.strategy_result import StrategyResult


class Strategy8bit(AbstractStrategy):
    CLASS_NAME = "Strategy8bit"

    def __init__(self, config, logger, utils, services):
        super().__init__(config, logger, utils, services)

    def process(self, content_type, payload):
        result = StrategyResult()
        result.payload_to_print = payload
        # Unencoded 8-bit ASCII
        self.logger.log("Unencoded 8-bit ASCII | Content-Type: " + str(content_type), Strategy8bit.CLASS_NAME)
        self.logger.log(f"***** RAW PAYLOAD {Strategy8bit.CLASS_NAME} *****")
        self.logger.log(payload + "\n")

        if self.config["payload_analysis"]:
            self.logger.log(f"***** PAYLOAD ANALYSIS {Strategy8bit.CLASS_NAME} *****")
            # TODO
            self.logger.log("8bit")
            self.logger.log("***** END ANALYSIS *****")
        return result
