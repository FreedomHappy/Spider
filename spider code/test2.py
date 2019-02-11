import requests
from lxml import html
url='https://movie.douban.com/top250?start=225&filter='
response=requests.get(url).content
selector=html.fromstring(response)
answer=selector.xpath("//div[@class='paginator']/span[@class='next']/a/@href")
if answer:
	print(answer)