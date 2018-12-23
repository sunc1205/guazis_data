import numpy as np
import pandas as pd
import os
import sys
import glob

from datetime import datetime
from datetime import timedelta

#dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
 
#df = pd.read_csv(infile, parse_dates=['datetime'], date_parser=dateparse)


#读入csv文件
def csv_list():
	path=sys.path[0]
	files=glob.glob(path+"/*.csv")
	for file in files:
		df=pd.read_csv(file,parse_dates=['上牌时间','年检到期','交强险','商业险到期'])
	return df

#加载品牌目录
def load_brand():
	with open('brand_catalog.txt','r',encoding='utf-8-sig') as f:
		d=f.readline()
	b=d.split(',')
	return b
	#print(type(b))

#加载车系目录
def load_cata():
	with open('cata_catalog.txt','r',encoding='utf-8-sig') as f:
		d=f.readline()
	b=d.split(',')
	return b
	#print(type(b))
	
	
# 品牌 车系处理
def catalog(df):
	
	b=load_brand()
	c=load_cata()
	# 品牌
	df['brand']=''
	df['catalog']=''
	df['款']=''
	
	df['款']=df["car_title"].str.findall('\d{4}款')
		
	for i in b:
		
		bool_list1=df["car_title"].str.match(i)
		df["brand"][bool_list1]=i

	for i in c:
		#print(i)
		bool_list1=df["car_title"].str.contains(i)
		df['catalog'][bool_list1]=i
	df.set_index('catalog','款','brand')
	return df
	#df.to_csv('ssss.csv')

def time(df):
	now =datetime.now()
	#print(type(now))
	dif1=now-pd.to_datetime(df['上牌时间'])
	print(dif1[0].days)

def fa(df):
	ss=df.groupby(by='catalog').count()
	print(ss.head(10))
	
	
	

if __name__ =="__main__":
	df=csv_list()
	
	#time(df)
	catalog(df)
	fa(df)
	#print(df)
	
