#!/usr/bin/env python

import urllib2
import time
import hashlib
import json
import sys

class reportSMS():
    def __init__(self):
        timestamp = self.gettime()
        appid = "18d74816eb6e47c7afe6c2a5c0cf5dc9"
        sid = "5928bfabf70b4a2d8e92bc34a69ba6af"
        token = "801c65d3bc3f4d868fc57113bbadc615"
        phoneNumber = "18674802640"
        self.header = {
            "Host" : "api.qingmayun.com",
            "Accept" : "application/json",
            "Content-Type" : "application/json;charset=utf-8"
        }

        self.param = {
            "templateSMS": {
                "appId" : appid,
                "templateId" : "20060055",
                "to" : "",
                "param" : ""
            }
        }
        sig = self.getMd5(sid, token, timestamp)
        self.url = "https://api.qingmayun.com/20141029/accounts/%s/SMS/templateSMS?sig=%s&timestamp=%s" % (sid, sig, timestamp)

    def gettime(self):
        now = time.strftime("%Y%m%d%H%M%S")
        return now

    def get_time_normal_format(self):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        return now

    def getMd5(self, ssid, ttoken, ttimestamp):
        md5 = hashlib.md5()
        md5.update((ssid + ttoken + ttimestamp))
        sig = md5.hexdigest()
        return sig

    def sendSMS(self):
        phonenumbers = []
        i = 1
        for item in sys.argv[1:]:
            if len(item) == 11 and item.isdigit():
                phonenumbers.append(item)
                i += 1
        print phonenumbers
        for item in sys.argv[i:]:
            self.param['templateSMS']['param'] += str(item) + " "
        self.param['templateSMS']['param'] += "        %s        " % (self.get_time_normal_format())
        for phone in phonenumbers:
            self.param['templateSMS']['to'] = phone
            data = json.dumps(self.param)
            req = urllib2.Request(self.url, headers=self.header, data=data)
            urllib2.urlopen(req, timeout=50)

if __name__ == "__main__":
    sendSMS = reportSMS()
    sendSMS.sendSMS()