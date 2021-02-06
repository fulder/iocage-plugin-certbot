#!/bin/sh

pip install -r /usr/local/certbot/requirements.txt

echo "0 0 * */2 *" python /usr/local/certbot/update_certs.py > new_cron

echo "Installation successful. Plugin config file: /usr/local/certbot/update_certs.yaml"

