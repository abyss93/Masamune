# Author: Abyss93

class PayloadAnalysisResult:

    def __init__(self):
        self.children = []
        self.tree_id = ""
        self.nest_level = -1  # -1 is the dummy root node to collect results
        self.strategies_results = []
        self.payload_headers = []
