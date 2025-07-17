import quopri

from content_transfer_encoding_strategies.abstract_strategy import AbstractStrategy


class StrategyQuotedPrintable(AbstractStrategy):
    CLASS_NAME = "StrategyQuotedPrintable"

    def __init__(self, config, logger, utils, services):
        self.services = services
        self.logger = logger
        self.utils = utils
        self.config = config

    def process(self, content_type, payload):
        # Encoded 7-bit ASCII
        self.logger.log("Quoted Printable | Content-Type: " + str(content_type), StrategyQuotedPrintable.CLASS_NAME)
        # join preserving \n because while it is useful not to have \n in base64, newlines are needed
        # to correctly process the body in quoted-printable elements (e.g. HTML code) https://www.rfc-editor.org/rfc/rfc2045#section-6.7
        body = ''.join(payload)
        decoded = quopri.decodestring(body).decode("utf-8")
        if self.config["print_payload"]:
            print(f"***** RAW PAYLOAD {StrategyQuotedPrintable.CLASS_NAME} *****")
            print(decoded + "\n")

        if self.config["payload_analysis"]:
            print(f"***** PAYLOAD ANALYSIS {StrategyQuotedPrintable.CLASS_NAME} *****")
            if self.config["debug"]: self.logger.log(body)
            res_print, res_domains = self.utils.find_urls("decoded_quopri", payload)
            if res_domains:
                matches = []
                for d in res_domains:
                    matches = matches + self.services["feed_service"].process_domain(d)
            # TODO
            print("***** END ANALYSIS *****")
