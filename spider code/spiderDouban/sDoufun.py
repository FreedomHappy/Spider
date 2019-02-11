#encoding: utf-8
import requests
import time
import random
from lxml import html
import os
from sqlDou import ConnDb


'''#创建主页类，抓取此电影主页的信息，并进行分析提取'''
class MovSubAna():
	def __init__(self,url):#初始化选择器
		header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
		}
		time.sleep(1)
		response=requests.get(url,headers=header).content
		self.selector=html.fromstring(response)
		self.url=url
		self.header=header
	def __selector(self,str):#创建解析函数
		get=self.selector.xpath(str)
		get='/'.join(get)
		return get
	def mName(self):#获取电影名
		name=self.__selector("//div[@id='content']/h1/span[1]/text()")
		if not name:
			name='电影名获取失败'
			print(name)
		return name
	def mInfo(self,path='1'):#电影信息,评分信息,海报
		if path=='1':
			path='F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/'
		#电影名
		name=self.mName()
		#电影基本信息
		director=self.__selector('//*[@id="info"]/span[1]/span[2]/a/text()')
		scenarist=self.__selector('//*[@id="info"]/span[2]/span[2]/a/text()')
		actor=self.__selector('//div[@id="info"]//span[@class="actor"]//a/text()')
		type=self.__selector('//div[@id="info"]//span[@property="v:genre"]/text()')
		area=self.__selector('//div[@id="info"]//span[text()="制片国家/地区:"]//following-sibling::text()[1]')
		language=self.__selector("//div[@id='info']//span[text()='语言:']//following-sibling::text()[1]")
		date=self.__selector("//div[@id='info']//span[text()='上映日期:']//following-sibling::span[@property='v:initialReleaseDate']/@content")
		length=self.__selector("//div[@id='info']//span[text()='片长:']//following-sibling::span[1]/@content")
		alias=self.__selector("//div[@id='info']//span[text()='又名:']//following-sibling::text()[1]")
		#电影评分信息
		totalsco=self.__selector("//div[@id='interest_sectl']//strong[@property]/text()")
		numpeople=self.__selector("//div[@id='interest_sectl']//a[@href='collections']/span/text()")
		better=self.__selector("//div[@id='interest_sectl']//div[@class='rating_betterthan']/a/text()")
		#电影URL
		url=self.url
		#电影海报
		imagepath=self.mImage(path)
		#组合成一个元组
		minfo=(name,director,scenarist,actor,type,area,language,date,length,alias,totalsco,numpeople,better,url,imagepath)
		return minfo
	def mImage(self,path='1'):#获取电影海报
		if path=='1':
			path='F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/'
		#解析图片地址
		image="//div[@id='mainpic']//img//@src"
		judge=self.selector.xpath(image)
		#准备下载图片
		if judge:#判断是否解析成功
			jpglink=judge[0]#取为字符串
			#print(jpglink)
			filename=str.split(jpglink,'/')[-1]
			filepath='%s%s'%(path,filename)
			#print(filepath)
			with open(filepath,'wb') as jpg:#开始下载图片
				time.sleep(0.1)
				jpg.write(requests.get(jpglink, headers=self.header).content)
		else:
			filepath='获取图片地址失败！'
			print(filepath)
		return filepath



'''电影评论相关操作'''
def mComment(movno):#爬取电影评论
		#从数据库中获取地址和电影序列
		select="select movno,murl from mSubject where movno=%s"%(movno)
		db=ConnDb()
		get=db.ExecSelect(select,1)
		movno=get[0]
		url=get[1]
		print(movno,url)
		#获取短评页地址
		res=requests.get(url).text
		sel=html.fromstring(res)
		judge=sel.xpath("//div[@id='comments-section']//span[@class='pl']/a/@href")
		curl=[]
		for i in range(5):#爬5页评论
			if judge:
				curl=curl+judge
			else :
				print('第%d评论爬取或解析失败!'%(i+1))
			url='https://movie.douban.com/subject/26752088/comments'+sel.xpath('//div[@id="paginator"]//a/@href')
			print(url)
			res=requests.get(url).text
			sel=html.fromstring(res)
			judge=sel.xpath("//div[@id='comments-section']//span[@class='pl']/a/@href")
		print(curl)
		'''
		#获取短评,封装数据
		res=requests.get(curl).text
		sel=html.fromstring(res)
		comments=sel.xpath("//div[@class='comment']//p/text()")
		data=[]
		for i in comments:
			data.append((movno,i))
		#print(data)
		#插入数据库
		insert='insert into mComment(movno,comtext)values(%s,%s)'
		con=ConnDb()
		con.ExecInsert(insert,data)
		print('评论爬取成功！')
		'''
def dbcomment(movno):#获取数据库评论
	select="select comtext from mComment where movno=%s"%(movno)
	db=ConnDb()
	get=db.ExecSelect(select)
	if not get:
		print('此电影还未获取评论！')
		return -1
	comm=[]
	for i in get:
		comm.append(i[0])
	#print(comm)
	return comm#返回字符串元素的列表

'''URL池相关操作'''
def insert_urlpool(urls):#插入URL池中，urls为字符串元素的列表
	data=[]
	n=1
	for url in urls:
		a=MovSubAna(url)
		name=a.mName()
		data.append((url,name))
		print('第%d条URL插入URLpool准备完成'%(n))
		n=n+1
	conn=ConnDb()
	insert='insert into movieurl(url,name)values(%s,%s)'
	conn.ExecInsert(insert,data)
def getAllurlpool():#获取URLpool中的所有URL
	con=ConnDb()
	select='select url from movieurl'
	urls=con.ExecSelect(select)
	return urls

def getUrlpoolInfo():#获取URL池信息
	con=ConnDb()
	select='select url,name from movieurl'
	info=con.ExecSelect(select)
	return info

'''电影基本信息相关操作'''
def insert_mSubject(urls,impath='1'):#将电影主页面全部minfo信息插入数据库,urls 可以是一个或多个URL,且必须是元素为字符串的列表
	if impath=='1':
		impath='F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/'
	con=ConnDb()
	insert='''insert into mSubject(movname,mdirector,mscenarist,mactor,mtype,marea,mlanguage,mdate,mlen,malias,mtotalsco,mnumpeople,mbetter,murl,mimage)
	values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''#插入操作
	minfos=[]
	n=1
	for i in urls:
		ana=MovSubAna(i)#构造解析器,i[0]将i这个元组取为URL字符串
		print(i)
		#print(ana.mInfo())
		minfos.append(ana.mInfo(impath))#将解析出来的一个元组数据加入minfos列表
		print('第%d部解析成功！'%(n))
		n=n+1
	con.ExecInsert(insert,minfos)#执行插入操作
	
def getMovieinfo():#获取数据库中的电影信息
	select='select *from mSubject'
	conn=ConnDb()
	minfo=conn.ExecSelect(select)
	return minfo

def update_mSubject(sql,data):#更新数据库
	conn=ConnDb()
	conn.ExecInsert(sql,data)

'''提取Top250URL'''
DouBanTop250_url='https://movie.douban.com/top250'
#提取Top250的所有电影介绍URL
def url_All(url):
	urls=url_SinglePage(url)#提取第一页的URL，存为一个列表
	#修改代理
	header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	#提取下一个页面的URL
	next=url
	while 1:
		time.sleep(1)
		response=requests.get(next,headers=header).content#请求http
		selector=html.fromstring(response)
		judge=selector.xpath("//div[@class='paginator']/span[@class='next']/a/@href")#解析下一页的地址
		if judge:
			next=DouBanTop250_url+judge[0]#得出下一页地址
			temp=url_SinglePage(next)#提取下一页的URL
			urls=urls+temp
		else:
			print('跳转下一页失败！')
			break
	return urls
#提取此Top250页面的所有电影主页面URL
def url_SinglePage(url):
	header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	time.sleep(1)
	response=requests.get(url,headers=header).content
	selector=html.fromstring(response)
	urls=[]
	for i in selector.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/@href'):
		urls.append(i)
	return urls
	



'''提取正在上映的电影（福州）的URL'''
NowPlaying_FuZhou='https://movie.douban.com/cinema/nowplaying/fuzhou/'
def nowPlaying(url):
	header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	response=requests.get(url,headers=header).content
	selector=html.fromstring(response)
	urls=[]
	for i in selector.xpath("//div[@id='nowplaying']//ul[@class='lists']//li[@class='stitle']/a/@href"):
		urls.append(i)
	return urls

'''创建IP池'''
#获取IP
def sIP(url):
	header={
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
	}
	res=requests.get(url,headers=header).text
	selector=html.fromstring(res)
	ips=[]
	for i in selector.xpath('//tr[@class]//td[2]/text()'):
		ips.append(i)
	protocol=[]
	for i in selector.xpath('//tr[@class]//td[6]/text()'):
		protocol.append(i)
	
	data=[]
	n=0
	for i in selector.xpath('//tr[@class]//td[3]/text()'):
		data.append((ips[n],i,protocol[n]))
		n=n+1
	print(data)
	conn=ConnDb()
	insert='insert into ipPool values(%s,%s,%s)'
	conn.ExecInsert(insert,data)
	
	
def main():
	#mComment()
	#insert_url(["https://movie.douban.com/subject/1292052/"])
	#print(getUrlpoolInfo())
	#print(getMovieinfo())
	#dbcomment('000001')
	#sIP('http://www.xicidaili.com/nn/1')
	mComment('000273')
	pass


if __name__=='__main__':
	main()
	
	
	
	
	
	
	

'''
遗留代码
(1)#对数据库进行更新
	path="F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/Top250/"
	urls=getAllurlpool()
	
	#下载图片并获取图片存储路径
	imagepath=[]
	for url in urls[0:50]:
		t=MovSubAna(url[0])
		imagepath.append(t.mImage(path))
	#print(imagepath)
	#准备更新数据
	data=[]
	for i in range(50):
		a=i+1
		tu=(imagepath[i],'000000'+str(a))
		data.append(tu)
	#print(data)
	#对数据库的mSubject表mimage字段进行更新
	strl="update mSubject set mimage=%s where movno=right(%s,6)"
	update_mSubject(strl,data)
(2)#插入正在福州上映的电影信息
	impath='F:/a软件工程学科文件/Python/spider code/DouData/Dmovie/Image/NowPlaying/'
	urls=nowPlaying(NowPlaying_FuZhou)
	insert_mSubject(urls,impath)
'''