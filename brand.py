import requests
from pyquery import PyQuery as pq
import json
import csv
import numpy as np
import pandas as pd
import time

# 获取网页响应
def get_one_page(url):
	cookies='uuid=acde11d7-f860-4413-b0b9-968b4c492022; ganji_uuid=7201852630120178900750; clueSourceCode=10103000312%2300; antipas=128t0s4899679W4k4688492A1328Vq; sessionid=b3250f1e-803b-41d8-898d-3aeb58c39d36; lg=1; _gl_tracker=%7B%22ca_source%22%3A%22-%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A5366926634%7D; cainfo=%7B%22ca_s%22%3A%22pz_baidu%22%2C%22ca_n%22%3A%22tbmkbturl%22%2C%22ca_i%22%3A%22-%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22%25e7%2593%259c%25e5%25ad%2590%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22scode%22%3A%2210103000312%22%2C%22ca_transid%22%3Anull%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22ca_b%22%3A%22-%22%2C%22ca_a%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22acde11d7-f860-4413-b0b9-968b4c492022%22%2C%22sessionid%22%3A%22b3250f1e-803b-41d8-898d-3aeb58c39d36%22%7D; cityDomain=xuzhou; preTime=%7B%22last%22%3A1545503933%2C%22this%22%3A1540047462%2C%22pre%22%3A1540047462%7D'
	jar=requests.cookies.RequestsCookieJar()
	for cookie in cookies.split(';'):
		key,value = cookie.split('=')
		jar.set(key,value)

	headers={
	#'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
	'Host':'www.guazi.com'
    }
	#print(url)
	response=requests.get(url,cookies=jar,headers=headers)
	if response.status_code != 200:
		print(response.status_code,'response failed')
	else:
		html=response.text
		return   html


def details(html):
	doc=pq(html)

	# 品牌
	catalog=doc('.dd-all.clearfix.js-brand.js-option-hid-info li')
	A_brand=catalog.find('label').parent().find('a')
	brand_lsit=[]
	for i in A_brand.items():
		brand_lsit.append(i.text())
	with open('brand_catalog.txt','w',encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(brand_lsit) 

	
# 主程序        
def main():
	domain='https://www.guazi.com/xuzhou/buy'
	#print(domain)
	html=get_one_page(domain)
	details(html)

				

# 主程序
if __name__ == "__main__":
	main() 
	
