# Author: Abyss93

class StrategyResult:

    def __init__(self):
        self.urls = []
        self.domains = []
        self.payload_to_print = ""
        self.domain_feed_matches: list[dict] = []
        self.hashes: list[dict] = []

    def __str__(self):
        return f"""
            URL: {self.urls}\n
            Domain: {self.domains}\n
            Payload to print: {self.payload_to_print}\n
            Domain Matches: {self.domain_feed_matches}\n
            Hashes: {self.hashes}
        """
