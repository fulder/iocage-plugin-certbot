import logging
import os
from subprocess import Popen

import yaml

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_LOCATION = os.path.join(CURRENT_DIR, "update_certs.yaml")
LOG_LOCATION = os.path.join(CURRENT_DIR, "update_certs.log")
CERTBOT_DIR = os.path.join(CURRENT_DIR, "certbot")

logger = logging.getLogger("update_certs")


class UpdateCert:

    def __init__(self):
        self.cfg = {}

    def main(self):
        self._load_config()
        self._setup_logger()
        logger.info(f"Config loaded from: {CONFIG_LOCATION}")

        self._cloudflare()

        logger.info("Cert updater script completed")

    def _load_config(self):
        with open(CONFIG_LOCATION, "r") as f:
            self.cfg = yaml.safe_load(f)

    def _setup_logger(self):
        log_level = self.cfg["log_level"]

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')

        logger.setLevel(log_level)
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(log_level)
        logger.addHandler(sh)

        fh = logging.FileHandler(LOG_LOCATION)
        fh.setFormatter(formatter)
        fh.setLevel(log_level)
        logger.addHandler(fh)

        logger.debug("Configured logger")

    def _cloudflare(self):
        domains = self.cfg["cloudflare"]["domains"]

        if domains is None:
            logger.info("No cloudflare domains found")
            return

        for domain in domains:
            if "api_key" not in domain:
                logger.error(f"Required 'api_key' property not found for domain: {domain}")
            if "domain_name" not in domain:
                logger.error(f"Required 'domain_name' property not found for domain: {domain}")

            # create temporary cloudflare ini file
            cloudflare_ini_path = os.path.join(CURRENT_DIR, "cloudflare_tmp.ini")
            with open(cloudflare_ini_path, 'w') as f:
                f.write(f"dns_cloudflare_api_token = {domain['api_key']}")

            certbot_command = [
                "certbot", "certonly",
                "--dns-cloudflare",
                "--dns-cloudflare-credentials", cloudflare_ini_path,
                "-d", domain["domain_name"]
            ]
            self._run_certbot_command(certbot_command)

            os.remove(cloudflare_ini_path)

    def _run_certbot_command(self, certbot_command):
        config_dir = os.path.join(CERTBOT_DIR, "config")
        work_dir = os.path.join(CERTBOT_DIR, "work")
        logs_dir = os.path.join(CERTBOT_DIR, "logs")

        certbot_command += [
            "--config-dir", config_dir,
            "--work-dir", work_dir,
            "--logs-dir", logs_dir,
        ]
        logger.info(f"Running certbot command: {certbot_command}")

        p = Popen(certbot_command)
        p.communicate()
        if p.returncode != 0:
            logger.error("Error during certbot command execution")
            raise RuntimeError()


if __name__ == "__main__":
    UpdateCert().main()
