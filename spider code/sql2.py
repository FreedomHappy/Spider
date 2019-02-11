# encoding: utf-8
import pymssql
from spider_douban import url_All
from spider_douban import movieName
from spider_douban import url_SinglePage

DouBanTop250_url='https://movie.douban.com/top250'

#连接初始化
sever='DESKTOP-0T3177R'
user='spider'
password='123'
database='douban'

try:
	conn=pymssql.connect(sever,user,password,database,'utf-8')#连接数据库
	cursor=conn.cursor()#建立游标
	insert='insert into movieurl(url,name) values(%s,%s)'#插入操作

	#将Top250的URL和电影名写入数据库
	urls=url_All('https://movie.douban.com/top250?start=200&filter=')
	for url in urls:
		data=[]
		for j in url:
			name=movieName(j)
			data.append((j,name))
		cursor.executemany(insert,data)
		conn.commit()
except Exception as ex:
	conn.rollback()
	raise ex
finally:
	conn.close()



'''
select='select * from movieurl'
cursor.execute(select)
get=cursor.fetchall()
print(get)
'''
'''
if __name__='__main__':
	main()
'''