from datetime import datetime


class Logger:

    def __init__(self, debug_enabled):
        self.debug_enabled = debug_enabled

    def log(self, debug_info, context=""):
        if self.debug_enabled:
            print(f"DEBUG | {datetime.today()} | {context} | {debug_info}")
