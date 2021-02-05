#!/bin/sh

log="/var/logs/iocage_certbot.log"
cloudflare_ini="/usr/local/certbot/.secrets/cloudflare.ini"

cloudflare_api_key=$(sed 's/dns_cloudflare_api_token = //g' ${cloudflare_ini})
cloudflare_domains=$(sed 's/dns_cloudflare_api_token = //g' ${cloudflare_ini})

certbot_command="certbot certonly"

if ! [ -z "$cloudflare_api_key" ]
then
    echo "Found cloudflare key" >> ${log}

    certbot_command="${certbot_command} --dns-cloudlflare --dns-cloudflare-credential ${cloudflare_ini} --dns-cloudflare-propagation-seconds 60"
    if sysrc -c -q cloudflare_domains
    then
      for domain in $(sysrc -n cloudflare_domains)
      do
        certbot_command="${certbot_command} -d ${domain}"
      done
    else
      echo "No CloudFlare domains found, please set the 'cloudflare_domains' variable" >> ${log}
      exit 1
    fi

    echo "Executing certbot command: ${certbot_command}" >> ${log}
    eval ${certbot_command} >> ${log}
fi