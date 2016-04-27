#!/usr/bin/env python2.7

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = "day9011@gmail.com"
receiver = ["329723954@qq.com"]

server = "smtp.gmail.com"
username = "day9011@gmail.com"
password = "day5673914"

message = MIMEText("zabbix alert service is stopped", "plain", "utf-8")
message['from'] = Header("day9011", "utf-8")
message['to'] = Header("to", "utf-8")

subject = "zabbix ct cloud"

smtp = smtplib.SMTP('smtp.gmail.com:587')
smtp.ehlo()
smtp.starttls()
smtp.login(username, password)
smtp.sendmail(sender, receiver, message.as_string())