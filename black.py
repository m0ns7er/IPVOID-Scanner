import re
import os
import sys
import time
from colorama import Fore, Back, Style
from pytictoc import TicToc
import concurrent.futures
import datetime
from bs4 import BeautifulSoup
import requests
from multiprocessing.pool import Pool
from concurrent.futures import ThreadPoolExecutor
from stem import Signal
from stem.control import Controller

t = TicToc()

threadlist = []
logfile = "%s-BLACKLISTED-IP.txt" % (sys.argv[2])

def write_log(filename, line):
    f = open(filename, "a+")
    f.write(line.strip() + "\n")
    f.close()

def check_ipvoid(ip,session):

 url = "https://www.ipvoid.com/ip-blacklist-check/"
 payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ip\"\r\n\r\n%s\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--" % (ip)
 headers = {
                'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
                'cache-control': "no-cache",
                'postman-token': "3ed8dfc1-6779-d4ed-30e0-d7f1cc1ed9ee"
    }
 response = session.request("POST", url, data=payload, headers=headers)
 data = response.text
# r1 = session.get('http://httpbin.org/ip')
# print(r1.text)

 if re.search(r'<span class="label label-danger">BLACKLISTED .*</span>',data, re.MULTILINE):
    region_re = re.search(r'<td>Continent</td><td>.*</td>',data,re.MULTILINE)
    region = region_re.group()
    region_final = BeautifulSoup(region, "html.parser")
    country_code_re = re.search(r'<tr><td>Country Code</td><td>.*</td></tr>',data,re.MULTILINE)
    country_code = country_code_re.group()
    country_code_final = BeautifulSoup(country_code, "html.parser")
    count = re.search(r'<span class="label label-danger">BLACKLISTED .*</span>',data,re.MULTILINE)
    count_eng = count.group()
    count_eng_final = BeautifulSoup(count_eng, "html.parser")
    tmpstr = 'BLACKLISTED IP : %s | Region : %s | Country Code : %s  | Engines : %s' % (ip,region_final.get_text().replace("Continent",""),country_code_final.get_text().replace("Country Code ",""),count_eng_final.get_text().replace("BLACKLISTED ",""))
    print(Fore.RED + tmpstr)
    write_log(logfile, tmpstr)
 elif re.search(r'<span class="label label-warning">BLACKLISTED .*</span>',data, re.MULTILINE):
    region_re = re.search(r'<td>Continent</td><td>.*</td>',data,re.MULTILINE)
    region = region_re.group()
    region_final = BeautifulSoup(region, "html.parser")
    country_code_re = re.search(r'<tr><td>Country Code</td><td>.*</td></tr>',data,re.MULTILINE)
    country_code = country_code_re.group()
    country_code_final = BeautifulSoup(country_code, "html.parser")
    count = re.search(r'<span class="label label-warning">BLACKLISTED .*</span>',data,re.MULTILINE)
    count_eng = count.group()
    count_eng_final = BeautifulSoup(count_eng, "html.parser")
    tmpstr = 'BLACKLISTED IP : %s | Region : %s | Country Code : %s  | Engines : %s' % (ip,region_final.get_text().replace("Continent",""),country_code_final.get_text().replace("Country Code ",""),count_eng_final.get_text().replace("BLACKLISTED ",""))
    print(Fore.RED + tmpstr)
    write_log(logfile, tmpstr)
 elif re.search(r'<span class="label label-success">POSSIBLY SAFE .*</span>',data, re.MULTILINE):
    region_re = re.search(r'<td>Continent</td><td>.*</td>',data,re.MULTILINE)
    region = region_re.group()
    region_final = BeautifulSoup(region, "html.parser")
    country_code_re = re.search(r'<tr><td>Country Code</td><td>.*</td></tr>',data,re.MULTILINE)
    country_code = country_code_re.group()
    country_code_final = BeautifulSoup(country_code, "html.parser")
    print(Fore.GREEN + 'SAFE IP : %s | Region : %s | Country Code : %s' % (ip,region_final.get_text().replace("Continent",""),country_code_final.get_text().replace("Country Code ","")))
 else :
   tmpstr = 'PRIVATE/INVALID IP : %s' % (ip)
   print(Fore.RED + tmpstr)

 switchIP()



lines = open(sys.argv[1]).readlines()
t.tic()

print('Scanning started....')



def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

session = requests.session()
session.proxies = {}
session.proxies['http']='socks5h://localhost:9050'
session.proxies['https']='socks5h://localhost:9050'

with Pool() as pool:
    with session as ses:
        pool.starmap(check_ipvoid, [(line.strip(), ses) for line in lines])

print(t.toc())
