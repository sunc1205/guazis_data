import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob

from datetime import datetime
from datetime import timedelta

#读入csv文件
def csv_list(filename):
	# path=sys.path[0]
	# files=glob.glob(path+"/*.csv")
	# for file in files:
		# 
	# return df
	df=pd.read_csv(filename,parse_dates=['上牌时间','年检到期','交强险','商业险到期'])
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
	df['car_brand']=''
	df['car_catalog']=''
	df['款']=''
	
	df['款']=df["car_title"].str.findall('\d{4}款')
		
	for i in b:
		
		bool_list1=df["car_title"].str.match(i)
		df["car_brand"][bool_list1]=i

	for i in c:
		bool_list1=df["car_title"].str.contains(i)
		df['car_catalog'][bool_list1]=i
	df=df.set_index('car_catalog','款','car_brand')

	df.to_csv('new.csv')
	return df
	

def time(df):
	
	now =datetime.now()
	dif1=now-pd.to_datetime(df['上牌时间'])
	print(type(dif1[0]),type(now))
	print(dif1)

def fa(df):
	brand=df['car_brand'].value_counts()
	catalog=df['car_catalog'].value_counts()
	df=df.set_index(['car_brand','car_catalog'])
	print(brand)

	
	

if __name__ =="__main__":
	#df=csv_list('2018-12-23-12.38.31guazi.csv')
	df=csv_list('new.csv')
	#time(df)
	#catalog(df)
	fa(df)
	#print(df)
	
