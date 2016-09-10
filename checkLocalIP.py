from requests import get
import socket
import smtplib


#Variables
to = 'bertmsanders@gmail.com'
gmail_user = 'mike@sanders-tech.com'
gmail_pwd = 'cs96080108/'
smtp_server = "smtp.gmail.com"
smtp_port = 587
get_local_IP_url='http://myip.dnsomatic.com'
get_DNS_addr="local.sanders-tech.com"


#Script Start

#Get Local IP Address
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
	print "Not a Match, sending notification"
	smtpserver = smtplib.SMTP(smtp_server,smtp_port)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Local IP Changed \n'
	msg = header + '\n The local IP changed from ' + DNS_IP + ' to ' + localIP + ' , please update DNS  \n\n'
	print gmail_user
	print to
	print msg
	smtpserver.sendmail(gmail_user, to, msg)
	print 'done sending email!'
	smtpserver.close()
else:
	print "IP's Match, Exiting"

