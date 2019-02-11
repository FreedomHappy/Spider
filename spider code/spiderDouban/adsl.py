import redis
import random

class RedisClient(object):
	def __init__(self,host=REDIS_HOST,port=REDIS_PORT):
		self.db=redis.Redis(host=host,port=port,password=REDIS_PASSWORD)
		self.proxy_key=PROXY_KEY
	def key(self,name):
		return'{key}:{name}'.format(key=self.proxy_key,name=name)
	def set(self,name,proxy):
		return self.db.set(self.key(name),proxy)
	def get(self,name):
		return self.db.get(self.key(name)).decode('utf-8')

	def post(self):
		token=self.get_body_argument('token',default=None,strip=False)
		port=self.get_body_argument('port',default=None,strip=False)
		name=self.get_body_argument('name',default=None,strip=False)
		if token==TOKEN and port:
			ip=self.request.remote_ip
			proxy=ip+':'+port
			print('Receive proxy',proxy)
			self.redis.set(name,proxy)
			self.test_proxies()
		elif token!=TOKEN:
			self.write('Wrong Token')
		elif not port:
			self.write('No Client Port')

	def all(self):
		keys=self.keys()
		proxies=[{'name':key,'proxy':self.get(key)}for key in keys]
		return proxies

	def random(self):
		items=self.all()
		return random.choice(items).get('proxy')

	def list(self):
		keys=self.keys()
		proxies=[self.get(key) for key in keys]
		return proxies

	def first(self):
		return self.get(self.keys()[0])
		
