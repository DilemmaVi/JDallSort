import re
import requests as req
from bs4 import BeautifulSoup 
import lxml
import pandas as pd
import time
import json


#打开list文档(文档内容是从京东全部商品分类：https://www.jd.com/allSort.aspx，中获取到的网页源码)
with open('list.txt','r',encoding='utf-8') as file:
	result=file.read()

#从list文档中匹配到所有商品分类
url_list=re.findall('list.jd.com/list.html\?cat\=\d+.\d+.\d+', result)

url_list=set(url_list)

#定义四级分类
type_one_list=[]
type_two_list=[]
type_three_list=[]
type_four_list=[]

#遍历匹配到的list链接
for url in url_list:
	try:
		#使用requests库请求数据
		r=req.get('http://'+url)

		#使用BeautifulSoup解析数据
		soup = BeautifulSoup(r.text, 'lxml')
		type_one=soup.find('a',{'class':'crumbs-link'}).get_text()
		type_two=soup.find('span',{'class':'curr'}).get_text()
		type_three=soup.find_all('span',{'class':'curr'})[1].get_text()
		type_four_div=soup.find('div',{'id':'J_selector'}).find_all('div',{'class':'sl-key'})

		#获取隐藏的四级分类list
		try:
			type_four_exts=[]
			type_four_exts=json.loads(re.findall('other_exts \=(\[.*\]);', str(soup))[0])
		except:
			pass

		#遍历获取正常的四级分类
		for html in type_four_div:
			try:
				type_four=html.find('span').get_text().replace('：','').replace(' ','')
			except Exception as e :
				print(e)
				continue
			type_one_list.append(type_one.replace(' ',''))
			type_two_list.append(type_two.replace(' ',''))
			type_three_list.append(type_three.replace(' ',''))
			type_four_list.append(type_four.replace(' ',''))
			print(type_one.replace(' ','')+"-"+type_two.replace(' ','')+"-"+type_three.replace(' ','')+"-"+type_four.replace(' ',''))
		
		#遍历获取隐藏的四级分类
		if type_four_exts:
			for ext in type_four_exts:
				type_four=ext['name']
				type_one_list.append(type_one.replace(' ',''))
				type_two_list.append(type_two.replace(' ',''))
				type_three_list.append(type_three.replace(' ',''))
				type_four_list.append(type_four.replace(' ',''))
				print(type_one.replace(' ','')+"-"+type_two.replace(' ','')+"-"+type_three.replace(' ','')+"-"+type_four.replace(' ',''))						
	except Exception as e:
		print(e)
		#异常捕获，记录出错url，待程序结束后统一处理
		with open('app.log','a') as file:
			file.write(url+'\n')
		time.sleep(3)

#使用pandas储存数据，导出文件为excel，后缀格式为xlsx
df=pd.DataFrame({'一级分类':type_one_list,'二级分类':type_two_list,'三级分类':type_three_list,'四级分类':type_four_list})
df.to_excel('result.xlsx')
	