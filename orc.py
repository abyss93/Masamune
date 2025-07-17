#!/usr/bin/python3

import argparse
import email

from check_services.dumb_service import DumbService
from check_services.feeds_service import FeedsService
from content_transfer_encoding_strategies.strategy_7bit import Strategy7bit
from content_transfer_encoding_strategies.strategy_8bit import Strategy8bit
from content_transfer_encoding_strategies.strategy_base64 import StrategyBase64
from content_transfer_encoding_strategies.strategy_binary import StrategyBinary
from content_transfer_encoding_strategies.strategy_fallback import StrategyFallback
from content_transfer_encoding_strategies.strategy_quoted_printable import StrategyQuotedPrintable
from check_services.alienvault_otx_service import AlienVaultOTXService
from check_services.abuseipdb_service import AbuseipDBService
from header_analysis.header_analyzer import HeaderAnalyzer
from utils.logger import Logger
from utils.utils import Utils
from utils.config_parser import ConfigParser
from view.UI import UI
from view.terminal_view import TerminalView


def check_for_duplicate_content_type_header(p_headers):
    result = ""
    for h_tuple in p_headers:
        header_key = h_tuple[0]
        header_value = h_tuple[1]
        if header_key != "Content-Type":
            continue
        result = header_value
        if "boundary" in header_value:
            return header_value
    return result


def process_payloads(email_msg, utils, logger, payload_strategies, view, nest_level=-1):
    nest_level += 1
    if isinstance(email_msg.get_payload(), str):
        payload_headers = email_msg.items()
        content_type_h = check_for_duplicate_content_type_header(payload_headers)
        payload_headers = dict(payload_headers)
        payload_headers["Content-Type"] = content_type_h
        payload_strategies["fallback"].process(payload_headers["Content-Type"], email_msg.get_payload())
    else:
        for i, p in enumerate(email_msg.get_payload()):
            print("***** START_PAYLOAD_" + str(nest_level) + "_" + str(i) + " *****")
            # https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
            # <<Each part starts with an encapsulation boundary, and then contains a body part consisting of header area, a blank line, and a body area>>
            payload_headers = p.items()
            # in some emails there could be duplicate Content-Type header, hence the dict casting would preserve only the last of them
            # but the discarded header could contain a boundary, this way part of the mail would not be considered
            # we need to give priority to analyze ALL the email contents, since this is a security tool, not a tool that checks if the email is RFC-compliant
            content_type_h = check_for_duplicate_content_type_header(payload_headers)
            payload_headers = dict(payload_headers)
            payload_headers["Content-Type"] = content_type_h
            view.print_headers(payload_headers.items())

            if "Content-Transfer-Encoding" in payload_headers:
                try:
                    payload_strategies[payload_headers["Content-Transfer-Encoding"]].process(payload_headers["Content-Type"],
                                                                                       p.get_payload())
                except KeyError:
                    # There are only five valid values for the Content-Transfer-Encoding header: "7bit", "8bit", "base64", 
                    # "quoted-printable" and "binary". The email is broken on purpose by the sender
                    print(
                        f"Error: Strategy not defined for -> Content-Transfer-Encoding: \"{payload_headers['Content-Transfer-Encoding']}\"."
                        f" EMAIL IS PROBABLY BROKEN ON PURPOSE BY THE SENDER."
                        f" DOING FALLBACK ON A GENERIC-ANALYSIS STRATEGY")
                    payload_strategies["fallback"].process(payload_headers["Content-Type"], p.as_string())
            if "Content-Type" not in payload_headers:
                # https://www.rfc-editor.org/rfc/rfc2045#section-5.2 defaults to: Content-type: text/plain; charset=us-ascii
                payload_strategies["fallback"].process(payload_headers["Content-Type"], p.as_string())
            elif payload_headers["Content-Type"] is not None and "boundary" in payload_headers["Content-Type"]:
                # nested payload, another boundary is present and a recursive call is needed for the next nest_level
                process_payloads(p, utils, logger, payload_strategies, view, nest_level)

            print("***** END_PAYLOAD_" + str(nest_level) + "_" + str(i) + " *****")


def execute(email_path, config_args):
    # read email file
    with open(email_path, mode="rt", encoding="utf-8") as f:
        email_msg = email.message_from_file(f)

    # initialize logger, configurations and utils
    logger = Logger(config_args["debug"])
    config_parser = ConfigParser(logger)
    config_file = config_parser.parse("./config.yml")
    api_keys = config_file["api_keys"]
    feed_folder_path = config_file["feed_folder_path"]
    email_address_whitelist = config_file["email_address_whitelist"]
    domains_whitelist = config_file["domains_whitelist"]
    utils = Utils(logger)
    # initialize check services
    services = {}
    feed_service = FeedsService(logger, feed_folder_path)
    feed_service.update()  # create feeds or update outdated ones
    services["feed_service"] = feed_service
    if api_keys["alienvault_otx"]:
        services["alienvault_otx"] = AlienVaultOTXService(logger, api_keys["alienvault_otx"])
    else:
        services["alienvault_otx"] = DumbService(logger, "AlienVault")
    if api_keys["abuseipdb"]:
        services["abuseipdb"] = AbuseipDBService(logger, api_keys["abuseipdb"])
    else:
        services["abuseipdb"] = DumbService(logger, "AbuseIPDB")
    # prepare views
    view = TerminalView(config_args["color"])
    # preparing strategies to analyze the various types of email payloads by RFC types + a genaral fallback 
    payload_strategies = {
        "base64": StrategyBase64(config_args, logger, utils, services),
        "quoted-printable": StrategyQuotedPrintable(config_args, logger, utils, services),
        "7bit": Strategy7bit(config_args, logger, utils, services),
        "8bit": Strategy8bit(config_args, logger, utils, services),
        "binary": StrategyBinary(config_args, logger, utils, services),
        "fallback": StrategyFallback(config_args, logger, utils, services)
    }
    header_analyzer = HeaderAnalyzer(logger, utils, services, email_address_whitelist, domains_whitelist)

    # email processing
    headers = email_msg.items()
    if config_args["print_headers"]:
        print(
            "######################################################## HEADERS ########################################################")
        view.print_headers(headers)
        print(
            "#########################################################################################################################")
    if config_args["header_analysis"]:
        print(
            "\n################################################## ANALYSIS HEADERS #####################################################")
        header_analyzer.analyze(headers)
        print(
            "#########################################################################################################################")
    if config_args["payload_analysis"]:
        print(
            "\n######################################################## PAYLOADS #######################################################")
        process_payloads(email_msg, utils, logger, payload_strategies, view)
        print(
            "#########################################################################################################################")

    # user-interface only if requested by the user
    if config_args["user_interface"]:
        ui = UI()
        ui.render(headers)


if __name__ == "__main__":
    LOGO = "\033[35m           ▄▄▄   ▄▄·\033[0m\n" \
           "\033[35m     ▪     ▀▄ █·▐█ ▌▪\033[0m\n" \
           "\033[35m      ▄█▀▄ ▐▀▀▄ ██ ▄▄\033[0m\n" \
           "\033[35m     ▐█▌.▐▌▐█•█▌▐███▌\033[0m\n" \
           "\033[35m      ▀█▄▀▪.▀  ▀·▀▀▀\033[0m\n" 
    print(LOGO)
    parser = argparse.ArgumentParser(description="\033[35m -- ORC -- Email Forensic Tool --\033[0m\n",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("email_path", type=str, help="Path of the email to analyze (EML format)")
    parser.add_argument("-H", "--print-headers", help="Print email headers in a friendly way",
                        action="store_true",
                        default=True)
    parser.add_argument("-b", "--header-analysis", help="Analysis of headers", action="store_true")
    parser.add_argument("-a", "--payload-analysis", help="Payload analysis: hashes, URLs...", action="store_true")
    parser.add_argument("-p", "--print-payload",
                        help="Print email payloads as they are. This only works if --payload-analysis is set.",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="Debug info to stdout", action="store_true")
    parser.add_argument("-c", "--color", help="Some output sections are printed using terminal colors",
                        action="store_true")
    parser.add_argument("-x", "--user-interface", help="Display Headers in a window", action="store_true")
    args = parser.parse_args()
    config_args = vars(args)

    execute(args.email_path, config_args)
