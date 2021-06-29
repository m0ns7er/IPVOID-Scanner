import http.client
import re
import os
import sys
import time
from colorama import Fore, Back, Style


def check_ipvoid(ip):
 conn = http.client.HTTPSConnection("www.ipvoid.com")
 payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ip\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (ip)
 headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'cache-control': "no-cache",
                'postman-token': "3ed8dfc1-6779-d4ed-30e0-d7f1cc1ed9ee"
    }
 conn.request("POST", "/ip-blacklist-check/", payload, headers)
    
 res = conn.getresponse()
    
 result = res.read()
    
 data = result.decode("utf-8")
    
 if re.search(r'<span class="label label-danger">.*</span>',data, re.MULTILINE):
    print(Fore.RED + 'BLACKLISTED IP : %s' % (ip))
 else:
    print(Fore.GREEN + 'SAFE IP : %s' % (ip))
        
        
        
lines = open(sys.argv[1]).readlines()
for line in lines:
    if line.strip() != "":
        check_ipvoid(line.strip())

        time.sleep(3)
