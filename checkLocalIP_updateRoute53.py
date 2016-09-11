from requests import get
import socket
import smtplib
import boto3


#Variables
to = 'to@email.com'
gmail_user = 'user@gmail.com'
gmail_pwd = '######'
smtp_server = "smtp.gmail.com"
smtp_port = 587
#use a different get-ip service if you like
get_local_IP_url='http://myip.dnsomatic.com'
get_DNS_addr="your_local_dns_name.com"

# AWS Settings
awsAccessKeyId="#####"
awsSecretAccessKey="#####"
hosted_zone_id='#####'
# Note that this is a fully-qualified domain name.
name_to_match = 'subdomain.domain.com.'
TTL=300



#Script Start

#Get Local IP Address:
localIP = get(get_local_IP_url).text

print "LocalIP = " + localIP


#Get DNS IP Address
ip_list = []
ais = socket.getaddrinfo(get_DNS_addr,0,0,0,0)

for result in ais:
  ip_list.append(result[-1][0])
ip_list = list(set(ip_list))

DNS_IP = ip_list[0]

print 'DNS IP = ' + DNS_IP

match = localIP == DNS_IP

print "DoIPsMatch = " + str(match)

if match != True:
	print "Not a Match, updating AWS, sending notification"
	#Initialilze Route53 connect
	
	client = boto3.client('route53', aws_access_key_id=awsAccessKeyId, aws_secret_access_key=awsSecretAccessKey)
	cont_code = {}

	response = client.change_resource_record_sets(
	    HostedZoneId = hosted_zone_id,
	    ChangeBatch={
        	'Comment': 'testing boto',
	        'Changes': [
        	    {
                	'Action': 'UPSERT',
	                'ResourceRecordSet': {
        	            'Name': name_to_match,
                	    'Type': 'A',
	                    'TTL': TTL,
	                    'ResourceRecords': [
        	                {
                	            'Value': localIP
                        	},
	                        ],
        	            }
	            },
        	    ]
	    }
	)
	
	
	print("DNS record status %s "  % response['ChangeInfo']['Status'])
	print("DNS record response code %s " % response['ResponseMetadata']['HTTPStatusCode'])


	smtpserver = smtplib.SMTP(smtp_server,smtp_port)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Local IP Changed \n'
	msg = header + '\n The local IP changed from ' + DNS_IP + ' to ' + localIP + ' , AWS Route53 DNS Was Updated  \n\n'
	print msg
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done sending email!'
	smtpserver.close()
else:
	print "IP's Match, Exiting"

