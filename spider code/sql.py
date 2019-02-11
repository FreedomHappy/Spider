#!/usr/bin/env python
# encoding: utf-8

"""
@author: 侠之大者kamil
@file: sqlserver.py
@time: 2016/5/31 9:08
"""
import pymssql
conn = pymssql.connect(host="DESKTOP-0T3177R",user="john",password="123",database="orderdb")
cur = conn.cursor()
if not cur:
    raise (NameError,"数据库连接失败")
cur.execute("SELECT  *from employee")
resList=[]
for i in cur.fetchall():
	print(i)

conn.close()
print(resList)