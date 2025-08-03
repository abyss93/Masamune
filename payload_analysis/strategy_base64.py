# Author: Abyss93

import base64

from payload_analysis.abstract_strategy import AbstractStrategy
from payload_analysis.strategy_result import StrategyResult


class StrategyBase64(AbstractStrategy):
    CLASS_NAME = "StrategyBase64"

    def __init__(self, config, logger, utils, services):
        super().__init__(config, logger, utils, services)

    def process(self, content_type, payload):
        result = StrategyResult()
        self.logger.log("BASE64 | Content-Type: " + str(content_type), StrategyBase64.CLASS_NAME)

        body = ''.join(payload).replace("\n", "")
        decoded = base64.b64decode(body)
        result.payload_to_print = decoded

        self.logger.log(f"***** RAW PAYLOAD {StrategyBase64.CLASS_NAME} *****", StrategyBase64.CLASS_NAME)
        self.logger.log(payload + "\n", StrategyBase64.CLASS_NAME)
        if self.config["payload_analysis"]:
            self.logger.log(f"***** PAYLOAD ANALYSIS {StrategyBase64.CLASS_NAME} *****", StrategyBase64.CLASS_NAME)
            self.logger.log(body, StrategyBase64.CLASS_NAME)
            hashes = self.utils.hashes_of(decoded)
            result.hashes.append(hashes)
            # print(decoded)
            # if self.config["find_urls"]: self.utils.find_urls(decoded)
            # TODO
            self.logger.log("***** END ANALYSIS *****", StrategyBase64.CLASS_NAME)
        return result
