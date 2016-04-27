#!/usr/bin/env python2.7

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = "18674802640@163.com"
receiver = ["329723954@qq.com"]

server = "smtp.163.com"
username = "18674802640"
password = "5673914"

message = MIMEText("zabbix alert service is stopped", "plain", "utf-8")
message['from'] = Header("day9011", "utf-8")
message['to'] = Header("to", "utf-8")

subject = "zabbix ct cloud"
message['subject'] = Header(subject, "utf-8")

smtp = smtplib.SMTP()
smtp.connect(server, 25)
smtp.login(username, password)
smtp.sendmail(sender, receiver, message.as_string())