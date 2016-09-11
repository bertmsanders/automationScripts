# automationScripts
General use automation scripts

checkLocalIP_updateRoute53.py
checkLocalIP.py

These scripts were written to replace a dynamic dns service. It compares the local public IP to a dns name, if it has changed, it connects to Route53 using the boto3 library and updates the A record with the new local public IP. This script should be run under cron, and does not require elevated privelages. I run it hourly, but you could run it on a different schedule if desired. Y

I would recommend using a spare/ throw-away gmail account to send the email, as this script currently stores the credentials in plain text

*** NOTE: AWS, including Route53 is billed by usage. You are responsible for all charges made, I assume no responsibility if you run this script in an infinite loop, or something else silly

*** NOTE: If the To address is gmail, you will probably have to add a filter to never put emails from that sender in spam. Gmail's spam filter did not like my email format apparently, even though the account sending it is a contact.

checkLocalIP.py is a version that only sends an email

Installation/ Setup for checkLocalIP_updateRoute53.py

Requires/ Tested with Python  2.7.9 on Ubuntu 16.04
Uses the AWS boto3 python library for Route53 updates, and smtplib to send email

If you don't have pip ->>
$ apt-get install python-pip

$ pip install boto3

update the variables in the script:

//Variables
to = 'to@email.com'
gmail_user = 'user@gmail.com'
gmail_pwd = '######'
smtp_server = "smtp.gmail.com"
smtp_port = 587
//use a different get-ip service if you like
get_local_IP_url='http://myip.dnsomatic.com'
get_DNS_addr="your_local_dns_name.com"

// AWS Settings (checkLocalIP_updateRoute53.py only)
awsAccessKeyId="#####"
awsSecretAccessKey="#####"
hosted_zone_id='#####'
// Note that this is a fully-qualified domain name.
name_to_match = 'subdomain.domain.com.'
TTL=300

Change file permissions:
$ chmod 770 /home/user/checkLocalIP_updateRoute53.py

Add to Crontab (the schedule below runs hourly at 10 minutes after the hour)
$ crontab -e

10 * * * * /usr/bin/python /home/user/checkLocalIP_updateRoute53.py
