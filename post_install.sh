#!/bin/sh

pip install -r /usr/local/certbot/requirements.txt

echo "0 0 * */2 *" python3.7 /usr/local/certbot/update_certs.py > new_cron
crontab new_cron
rm new_cron

echo "Installation successful. Plugin config file: /usr/local/certbot/update_certs.yaml"

