import logging

class credential_view:
    def __init__(self, log_file):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=self.log_file,
            filemode="a"
        )

    def display_message(self, message):
        print("[open-control] " + message)
        logging.info(message)        