import http.client
import re
import os
import sys
import time
from colorama import Fore, Back, Style
import concurrent.futures
import datetime
from bs4 import BeautifulSoup

threadlist = []

logfile = "%s" % (datetime.datetime.now())

def write_log(filename, line):
    f = open(filename, "a+")
    f.write(line.strip() + "\n")
    f.close()

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
    region_re = re.search(r'<td>Continent</td><td>.*</td>',data,re.MULTILINE)
    region = region_re.group()
    region_final = BeautifulSoup(region, "html.parser")
    country_code_re = re.search(r'<tr><td>Country Code</td><td>.*</td></tr>',data,re.MULTILINE)
    country_code = country_code_re.group()
    country_code_final = BeautifulSoup(country_code, "html.parser")
    tmpstr = 'BLACKLISTED IP : %s | Region : %s | Country Code : %s' % (ip,region_final.get_text().replace("Continent",""),country_code_final.get_text().replace("Country Code ",""))
    print(Fore.RED + tmpstr)
    write_log(logfile, tmpstr)
 else:
    print(Fore.GREEN + 'SAFE IP : %s' % (ip))




lines = open(sys.argv[1]).readlines()
for line in lines:
    if line.strip() != "":

        check_ipvoid(line.strip())

        time.sleep(3)
