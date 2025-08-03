# Author: Abyss93

from payload_analysis.abstract_strategy import AbstractStrategy
from payload_analysis.strategy_result import StrategyResult


class StrategyBinary(AbstractStrategy):
    CLASS_NAME = "StrategyBinary"

    def __init__(self, config, logger, utils, services):
        super().__init__(config, logger, utils, services)

    def process(self, content_type, payload):
        result = StrategyResult()
        result.payload_to_print = payload
        # Unencoded 8-bit ASCII
        self.logger.log("Binary | Content-Type: " + str(content_type), StrategyBinary.CLASS_NAME)

        self.logger.log(f"***** RAW PAYLOAD {StrategyBinary.CLASS_NAME} *****", StrategyBinary.CLASS_NAME)
        self.logger.log(payload + "\n", StrategyBinary.CLASS_NAME)

        if self.config["payload_analysis"]:
            self.logger.log(f"***** PAYLOAD ANALYSIS {StrategyBinary.CLASS_NAME} *****", StrategyBinary.CLASS_NAME)
            # TODO
            hashes = self.utils.hashes_of(payload)
            result.hashes.append(hashes)
            self.logger.log("***** END ANALYSIS *****", StrategyBinary.CLASS_NAME)
        return result
