import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import glob

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']


from datetime import datetime
from datetime import timedelta

#读入csv文件
def csv_list(filename):
	# path=sys.path[0]
	# files=glob.glob(path+"/*.csv")
	# for file in files:
		# 
	#return df
	df=pd.read_csv(filename,parse_dates=['上牌时间','年检到期','交强险','商业险到期'])
	return df

def csv_list01(filename):
	# path=sys.path[0]
	# files=glob.glob(path+"/*.csv")
	# for file in files:
		# 
	# return df
	df=pd.read_csv(filename)
	#df=pd.read_csv(filename,index_col=['car_brand','car_catalog'])
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
	df=df.set_index(['car_brand','car_catalog'])

	df.to_csv('new.csv')
	return df
	

def time(df):
	
	now =datetime.now()
	dif1=now-pd.to_datetime(df['上牌时间'])
	print(type(dif1[0]),type(now))
	print(dif1)

def fa(df):
	
	#品牌排序
	gd1=df['car_brand'].value_counts(ascending=True)
	gd1.nlargest(20).plot(label='',kind='barh',subplots=True,stacked=True)
	plt.savefig('品牌汇总.png')
	plt.close()
	
	#车系排序
	gd0=df['car_catalog'].value_counts(ascending=True)
	gd0.nlargest(20).plot(label='',kind='barh',subplots=True,stacked=True)
	plt.savefig('车系汇总.png')
	plt.close()
	
	#gd1=df.groupby(['car_brand']).count()
	

	#gd2=gd2.loc[[x for x in gd1.nlargest(2).index]]['car_catalog'].value_counts(ascending=False)
	
	# fig=plt.figure()
	
	# ax1=fig.add_subplot(221) #2*2的图形 在第一个位置

	# ax2=fig.add_subplot(222)

	# ax3=fig.add_subplot(223)

	# ax3=fig.add_subplot(224)

	#品牌下的车系排序
	gd2=df.set_index('car_brand')
		
	for x in gd1.nlargest(10).index:
		plt.figure()
		gd3=gd2.loc[x]['car_catalog'].value_counts(ascending=False)
		#print(gd3)
		gd3.plot(label='',kind='barh')
		plt.savefig(x+'.png')
		plt.close()

	
	

if __name__ =="__main__":
	#df=csv_list('2018-12-27-20.12.05guazi.csv')
	df=csv_list01('new.csv')
	fa(df)
	#catalog(df)
	#
	#time(df)
	#
	#fa(df)
	#print(df)
	
