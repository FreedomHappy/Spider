#Dec 31st 2010
#-*- coding: utf-8 -*-

import requests
import json
from lxml import html
from lxml import etree
import sys 
import io
import re
import time
DouBanTop250_url='https://movie.douban.com/top250'


#提取top250的所有电影介绍URL
def url_All(url):
	url1=[]
	url1=url_SinglePage(url)#提取第一页的URL，存为一个列表
	urls=[]
	urls.append(url1)#将上述URL列表加入URLS作为第一个URL集
	#修改代理
	header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	#提取下一个页面的URL
	next=url
	while 1:
		time.sleep(2)
		response=requests.get(next,headers=header).content#请求http
		selector=html.fromstring(response)
		judge=selector.xpath("//div[@class='paginator']/span[@class='next']/a/@href")#解析下一页的地址
		if judge:
			next=DouBanTop250_url+judge[0]#得出下一页地址
			temp=url_SinglePage(next)#提取下一页的URL
			urls.append(temp)
		else:
			break
	return urls

#提取此top250页面的所有电影主页面URL
def url_SinglePage(url):
	header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	time.sleep(2)
	response=requests.get(url,headers=header).content
	selector=html.fromstring(response)
	urls=[]
	for i in selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href'):
		urls.append(i)
	return urls

#提取主页面的电影名
def movieName(urls):
	response=requests.get(urls).content
	selector=html.fromstring(response)
	title=(selector.xpath('//*[@id="content"]/h1/span[1]/text()'))
	if not title:
		title=['电影名获取失败']
	return title
		

def header(referer):
    headers = {
        'Host': 'https://www.douban.com/',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/59.0.3071.115 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers
	
	
def main():
	header={
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	url='https://movie.douban.com/subject/1292720/'
	response=requests.get(url,headers=header).content
	selector=html.fromstring(response)
	data=selector.xpath('//*[@id="content"]/h1/span[1]/text()')
	print(data)

if __name__=='__main__':
	main()

	
	