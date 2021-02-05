Iocage plugin for automatic cert validation using certbot and CloudFlare

# Testing manually
In freenas shell run:

* fetch https://raw.githubusercontent.com/fulder/iocage-plugin-index/certbot-plugin/certbot.json
* iocage fetch -P certbot.json --name certbot dhcp=on