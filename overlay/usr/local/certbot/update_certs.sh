#!/bin/sh

log = "/var/logs/iocage_certbot.log"
cloudflare_ini = "/usr/local/certbot/.secrets/cloudflare.ini"

cloudflare_api_key=$(sed 's/dns_cloudflare_api_token = //g' ${cloudflare_ini})

if ! [ -z "$cloudflare_api_key" ]
then
    echo "Found cloudflare key" >> ${log}
    certbot certonly \
      --dns-cloudflare \
      --dns-cloudflare-credential ${cloudflare_ini} \
      --dns-cloudflare-propagation-seconds 60 \
      -d example.com
fi