#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pprint
import requests
import subprocess
from getpass import getpass
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


IP_count = {}

subprocess.call('cat /var/log/nginx/access.log | cut -d" " -f1 > output.txt', shell=True)

with open('output.txt', 'r') as f:
        data = f.read()
        data = data.split("\n")

for line in data:
        ip  = line.strip()
        if ip == '':
                pass
        elif ip not in IP_count:
                IP_count[ip] = 1
        else:
                IP_count[ip] += 1


output = sorted(IP_count.items(), key=lambda x: x[1], reverse=True)

f = open('message.txt','w')
for item in output:
        r = requests.get("http://ip-api.com/json/" + item[0])
        data = r.json()
        f.write('IP: %s\n' % item[0])
        f.write('Connections: %s\n' % item[1])
        try:
                f.write('Location: %s, %s\n' % (data['city'], data['country']))
        except:
                pass
        f.write('\n')
f.close()


def mail_ips():
    '''
    email ips to myself
    '''
    s = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=120)
    s.starttls()

    while True:
        try:
            s.login('redacted@gmail.com','redacted-password')
            break
        except:
            print("Authentication failed... try again.")

    print("Emailing logged IPs...")
    msg = MIMEMultipart()
    f = open('message.txt','r')
    message = f.read()
    msg['From']'redacted@gmail.com'
    msg['To']='redacted@gmail.com'
    msg['Subject']="Nginx - IP Connection Logging"
    msg.attach(MIMEText(message, 'plain'))
    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

mail_ips()
