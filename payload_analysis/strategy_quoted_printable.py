# Author: Abyss93

import quopri

from payload_analysis.abstract_strategy import AbstractStrategy
from payload_analysis.strategy_result import StrategyResult
from utils.utils import Utils


class StrategyQuotedPrintable(AbstractStrategy):
    CLASS_NAME = "StrategyQuotedPrintable"

    def __init__(self, config, logger, utils, services):
        super().__init__(config, logger, utils, services)

    def process(self, content_type, payload):
        result = StrategyResult()
        # Encoded 7-bit ASCII
        self.logger.log("Quoted Printable | Content-Type: " + str(content_type), StrategyQuotedPrintable.CLASS_NAME)
        # join preserving \n because while it is useful not to have \n in base64, newlines are needed
        # to correctly process the body in quoted-printable elements (e.g. HTML code) https://www.rfc-editor.org/rfc/rfc2045#section-6.7
        
        body = ''.join(payload)
        charset = Utils.get_charset_from_content_type_header(str(content_type))
        # default to utf-8 just in case...
        decoded = quopri.decodestring(body).decode("utf-8")
        # ...but if the charset has been specified, and should always be the case...
        if charset is not None:
            decoded = quopri.decodestring(body).decode(charset)
        
        result.payload_to_print = decoded

        self.logger.log(f"***** RAW PAYLOAD {StrategyQuotedPrintable.CLASS_NAME} *****",
                        StrategyQuotedPrintable.CLASS_NAME)
        self.logger.log(decoded + "\n", StrategyQuotedPrintable.CLASS_NAME)

        if self.config["payload_analysis"]:
            self.logger.log(f"***** PAYLOAD ANALYSIS {StrategyQuotedPrintable.CLASS_NAME} *****",
                            StrategyQuotedPrintable.CLASS_NAME)
            self.logger.log(body, StrategyQuotedPrintable.CLASS_NAME)
            urls, domains = self.utils.find_urls_and_domains("decoded_quopri", decoded)
            matches = []
            if domains:
                for d in domains:
                    matches.extend(self.process_domain(d))
                self.logger.log(f"Matches: {matches}", StrategyQuotedPrintable.CLASS_NAME)
            result.domain_feed_matches = matches
            result.urls = urls
            result.domains = domains
            self.logger.log("***** END ANALYSIS *****", StrategyQuotedPrintable.CLASS_NAME)
        return result
