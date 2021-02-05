import logging
import os

import yaml

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_LOCATION = os.path.join(CURRENT_DIR, "update_certs.yaml")

logger = logging.getLogger("update_certs")


class UpdateCert:

    def __init__(self):
        self.cfg = {}

    def main(self):
        self._load_config()
        self._setup_logger()

    def _load_config(self):
        with open(CONFIG_LOCATION, "r") as f:
            self.cfg = yaml.safe_load(f)

    def _setup_logger(self):
        log_level = self.cfg["log_level"]
        log_location = self.cfg["log_location"]

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

        logger.setLevel(log_level)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(log_level)
        logger.addHandler(sh)

        fh = logging.FileHandler(log_location)
        fh.setFormatter(formatter)
        fh.setLevel(log_level)
        logger.addHandler(fh)


if __name__ == "__main__":
    UpdateCert().main()
