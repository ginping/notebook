import redis


class Base(object):
	def __init__(self):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


class TestString(Base):
	
	def test_set(self):
		result = self.r.set('user', 'php')
		return result

	def test_get(self):
		result = self.r.get('user')
		return result

	def test_mset(self):
		dic = {
			'name': 'ph',
			'age': 19,
			'sex': 'male'
		}
		result = self.r.mset(dic)
		return result

	def test_mget(self):
		li = ['name', 'age', 'sex']
		result = self.r.mget(li)
		return result

	def test_del(self):
		li = ['name', 'age', 'sex']
		for i in li:
			result = self.r.delete(i)
		return result


class TestList(Base):

	def test_push(self):
		tup = ['Amy', 'Alice', 'Jhon', 'Jack']
		result = self.r.lpush('l_name', *tup)
		# return result
		result = self.r.lrange('l_name', 0, -1)
		return result

	def test_pop(self):
		result = self.r.lpop('l_name')
		return result


class TestSet(Base):

	def test_sadd(self):
		li = ['snake', 'cat', 'dog']
		result = self.r.sadd('youset', *li)
		return result

	def test_srem(self):
		li = ['snake', 'cat', 'tiger', 'pandas']
		result = self.r.srem('myset', *li)
		return result

	def test_sinter(self):
		result = self.r.sinter('myset', 'youset')
		return result

	def test_sunion(self):
		result = self.r.sunion('myset', 'youset')
		return result


def main():
	# str_obj = TestString()
	# print(str_obj.test_set())
	# print(str_obj.test_get())
	# print(str_obj.test_mset())
	# print(str_obj.test_mget())
	# print(str_obj.test_del())

	# list_obj = TestList()
	# print(list_obj.test_push())
	# print(list_obj.test_pop())

	# set_obj = TestSet()
	# print(set_obj.test_sadd())
	# print(set_obj.test_srem())
	# print(set_obj.test_sinter())
	# print(set_obj.test_sunion())

if __name__ == '__main__':
	main()