import requests
from pyquery import PyQuery as pq
import json
import csv
import numpy as np
import pandas as pd


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
	print(url)
	response=requests.get(url,cookies=jar,headers=headers)
	if response.status_code != 200:
		print(response.status_code,'response failed')
	else:
		html=response.text
		return   html




# 获取总的页数             
def get_total_pages(url):
	html=get_one_page(url)
	doc=pq(html)
	a=doc.find('.next').parent().prev().find('span').text() 
	if a:
		return a
	else:
		return str(1)
# 获取车详情页的url,并请求返回html
def get_links(url):
	html=get_one_page(url)
	doc=pq(html)
	carlist=doc('.carlist.clearfix.js-top li a')
	for i in carlist.items():
		t=i.attr('href')
		links='https://www.guazi.com'+t
		html=get_one_page(links)
		yield html

# 解析车详情并返回相关值
def get_car_details(html):
	doc=pq(html)

	# 获取标题
	title=doc('.titlebox')
	title.find('span').remove()
	car_tilte=title.text()
	print(car_tilte)
	# 车主报价
	car_prices=doc('.pricestype').text()
	#print(car_prices)
	# 车主报价
	car_newprices=doc('.newcarprice').text()
	#print(car_newprices)
	
	# 获取其他信息
	car_info=doc('.basic-eleven.clearfix div')
	car_info.find("em").remove()
	car_list=car_info.text()
	d=car_list.split()[:-1]
	car_info=doc('.basic-eleven.clearfix li')
	car_info.find("div").remove()
	car_list=car_info.text()
	e=car_list.split()[0:len(d)]
	#print(len(e),len(d))
	#dict={}
	d.append(car_prices)
	d.append(car_newprices)
	'''
	for i in range(len(e)):
		dict.setdefault(e[i],d[i])
	dict.setdefault('car_prices',car_prices)
	dict.setdefault('car_newprices',car_newprices)
	'''
		
	#print(d)
	return d
	#yield data


# 保存数据到csv文件
def write_to_csv00(data,car):
	#用列表和元组
	filename=str(car)+'.csv'
	fieldnames=[u'上牌时间',u'表现里程',u'上牌地',u'迁入地为准',u'变速箱',u'排量',u'登记为准',u'看车地址',u'年检到期',u'交强险',u'商业险到期',u'car_prices','car_newprices']
	with open(filename,'a',newline='',encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fieldnames) 

	
# 保存数据到csv文件
def write_to_csv01(data,car):
	#用列表和元组
	filename=str(car)+'.csv'
	with open(filename,'a',newline='',encoding='utf-8-sig') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(data) 
	
	
# 主程序        
def main(car):
	base_url='https://www.guazi.com/xuzhou/'
	url=base_url+car
	print(url)
	page_total=eval(get_total_pages(url))
	k=0
	for i in range(1,page_total+1):
		url=base_url+car+'/o'+str(i)
		print("---------1-----") 
		#return
		flag=get_links(url)
		if flag:
			for car_html in get_links(url):
				data=get_car_details(car_html)
				if k!=0:
					write_to_csv01(data,car)
				else:
					write_to_csv00(data,car)
				k+=1
				

# 主程序
if __name__ == "__main__":
	# 车系
	carlist=[
	'langyi','golf','suteng','dazhong-polo','tuguan','passat',
	'baolai','lamando','dazhong-cc',
	'yinglangxt','buick-junyue','buick-junwei'
	]

	for carc in carlist:
		main(carc)
