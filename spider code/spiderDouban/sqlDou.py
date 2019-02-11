#encoding: utf-8

import pymssql

#连接数据库类
class ConnDb():
	def __init__(self):#初始连接信息
		self.host='DESKTOP-0T3177R'
		self.user='spider'
		self.psd='123'
		self.db='douban'
	def __Connect(self):#连接数据库
		if not self.db:
			raise(NameError,"没有设置数据库信息")
		self.conn=pymssql.connect(self.host,self.user,self.psd,self.db,"utf8")
		cursor=self.conn.cursor()#建立游标
		if not cursor:
			raise(NameError,"连接数据库失败")
		else:
			return cursor
	def ExecInsert(self,sql,data):#插入数据或更新数据,data为元素为元组的列表
		try:
			cur=self.__Connect()
			for i in data:
				cur.execute(sql,i)
			self.conn.commit()
		except Exception as ex:
			self.conn.rollback()
			raise ex
		finally:
			cur.close()
			self.conn.close()
	def ExecSelect(self,sql,num=2):#查询数据,
		try:
			cur=self.__Connect()
			cur.execute(sql)
			if num==1:
				getlist=cur.fetchone()#num为1返回元组
			else:
				getlist=cur.fetchall()#num大于1返回元素为元组的列表
			self.conn.commit()
		except Exception as ex:
			self.conn.rollback()
			raise ex
		finally:
			cur.close()
			self.conn.close()
			return getlist



