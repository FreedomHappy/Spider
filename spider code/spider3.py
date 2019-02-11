import io  
import sys 
import requests
import json
import time
from lxml import html
from multiprocessing.dummy import Pool as ThreadPool
#r=requests.get('https://www.douban.com/')
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') # 改变标准输出的默认编码  


def get_page_number(num):
	#构建函数，用来查找该页内所有图片集的详细地址。
	#目前一页包含15组套图，所以应该返回包含15个链接的序列。
	url='http://www.mmjpg.com/home/'+num
	#构造每个分页的网址
	response=requests.get(url).content
	'''调用requests库，获取二进制的相应内容。
	注意，这里使用.text方法的话，下面的html解析会报错，大家可以试一下。
	这里涉及到.content和.text的区别了。
	简单说，如果是处理文字、链接等内容，建议使用.text，
	处理视频、音频、图片等二进制内容，建议使用.content。
	至于更详细的区别，就又可以写一篇文章了。'''
	
	selector=html.fromstring(response)
	#使用lxml.html模块构建选择器，
	'''主要功能是将二进制的服务器相应内容response
	转化为可读取的元素树（element tree）。
	lxml中就有etree模块，是构建元素树用的。
	如果是将html字符串转化为可读取的元素树，
	就建议使用lxml.html.fromstring，毕竟这几个名字应该能大致说明功能了吧。'''
	urls=[]
	for i in selector.xpath("//ul/li/a/@href"):
	#利用xpath定位到所有的套图的详细地址
		urls.append(i)
		break
		#遍历所有地址，添加到容器中
	return urls
	
	
def get_image_title(url):
	#现在进入到套图的详情页面了，现在要把套图的标题和图片总数提取出来
	response=requests.get(url).content
	selector=html.fromstring(response)
	image_title=selector.xpath("//h2/text()")[0]
	#需要注意的是，xpath返回的结果都是序列，所以需要使用[0]进行定位
	return image_title
	
def get_image_amount(url):
	#这里就相当于重复造轮子了，因为基本的代码逻辑跟上一个函数一模一样。
	'''
	想要简单的话就是定义一个元组，
	然后把获取标题、获取链接、获取图片总数的3组函数的逻辑揉在一起，
	最后将结果作为元组输出。
	不过作为新手教程，还是以简单易懂为好吧。想挑战的同学可以试试写元组模式
	'''
	response=requests.get(url).content
	selector=html.fromstring(response)
	image_amount=selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
	#a标签的倒数第二个区块就是图片集的最后一页，也是图片总数，所以直接取值就可以
	return image_amount
	
def get_image_detail_website(url):
	response=requests.get(url).content
	selector=html.fromstring(response)
	image_detail_websites=[]
	image_amount=selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
	
	for i in range(int(image_amount)):
		image_detail_link='{}/{}'.format(url,i+1)
		response=requests.get(image_detail_link).content
		sel=html.fromstring(response)
		image_download_link=sel.xpath("//div[@class='content']/a/img/@src")[0]
		image_detail_websites.append(image_download_link)
	return image_detail_websites
	
def header(referer):
    headers = {
        'Host': 'i.meizitu.net',
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Referer': '{}'.format(referer),
    }
    return headers
def download_image(image_title,image_detail_websites):
	num=1
	amount=len(image_detail_websites)
	for i in image_detail_websites:
		filename='C:\\Users\\傻豪\\Pictures\\Saved Pictures\\%s%s.jpg'%(image_title,num)
		print('正在下载图片：%s第%s/%s张，'%(image_title,num,amount))
		with open(filename,'wb') as f:
			f.write(requests.get(i,headers=header(i)).content)
			time.sleep(2)
		num+=1

def download(link):
	download_image(get_image_title(link),get_image_detail_website(link))

if __name__=='__main__':
	page_number=input('请输入爬取的页码：')
	link=get_page_number(page_number)
	with ThreadPool(4) as Pool:
		Pool.map(download,link)
		
		
		
