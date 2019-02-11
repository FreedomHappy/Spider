#encoding=utf-8

import requests
from lxml import html
import os
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
url='https://movie.douban.com/subject/1292052/'
#解析图片地址
res=requests.get(url)
sel=html.fromstring(res.content)
image="//div[@id='mainpic']//img//@src"
judge=sel.xpath(image)
if judge:#判断是否解析成功
	jpglink=judge[0]#取为字符串
	#print(jpglink)
	filename=str.split(jpglink,'/')[-1]
	filepath='F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/Top250/%s'%(filename)
	#print(filepath)
	with open(filepath,'wb') as jpg:#开始下载图片
		jpg.write(requests.get(jpglink, headers=headers).content)
else:
	print('获取图片地址失败！')