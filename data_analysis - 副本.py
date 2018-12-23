import numpy as np
import pandas as pd
import os
import sys
import glob

#读入csv文件
def csv_list():
	path=sys.path[0]
	files=glob.glob(path+"/*.csv")
	for file in files:
		df=pd.read_csv(file)
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
	
	df['款']=''
	df['款*']=''
	df['款']=df["car_title"].str.findall('\d{4}款')
	df['款*']=df["car_title"].str.findall('\d{4}款.*')
	
	df['catalog']=''
	
	for i in b:
		
		bool_list1=df["car_title"].str.match(i)
		df["brand"][bool_list1]=i
		df['catalog'][bool_list1]=df["car_title"][bool_list1].str.lstrip(i).str.lstrip(i)


		
	#list=df["car_title"].str.match('5')
	print(df['catalog'])
		#break
	#print(df.head(12)["brand"],df.head(12)["car_title"])
	
	# 车系
	#df['catalog']=''
	#print(df['catalog'].shape)
	#list2=df['car_title'].str.match('20')
	#print(df['catalog'])
	#print(df['car_title'].str.contains(df['brand']))
	#df['catalog']=df["car_title"].str.match()
	
	

	
	
	

if __name__ =="__main__":
	df=csv_list()
	catalog(df)
	#print(df)
	
