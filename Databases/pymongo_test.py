from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId


class TestMongo(object):

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client.news

	def add_one(self):
		''' 新增数据 '''
		post = {
		    'title': 'update',
		    'content': '博客内容, ....',
		    'created_at': datetime.now()
		}
		return self.db.news.insert_one(post)

	def get_one(self):
		''' 查询一条数据 '''
		return self.db.news.find_one()

	def get_more(self):
		''' 查询多条数据 '''
		return self.db.news.find()

	def get_one_from_oid(self, oid):
		''' 根据记录的ID来获取数据 '''
		return self.db.news.find_one({'_id': ObjectId(oid)})

	def update(self):
		''' 修改数据 '''
		# 修改一条数据
		return self.db.news.update_one({'title':'update'}, {'$set':{'title':'update_new'}})	
		# 修改多条数据
		# return self.db.news.update_many({ }, {'$set':{ }})

	def delete(self):
		''' 删除数据 '''
		# 删除一条数据
		rest = self.db.news.delete_one({'title':'update'})
		# 删除多条数据
		# rest = self.db.news.delete_many({'is_valid':0})
		return rest


def main():
	obj = TestMongo()
	# rest = obj.add_one()
	# print(rest.inserted_id)

	# rest = obj.get_one()
	# print(rest)

	# rest = obj.get_more()
	# for item in rest:
	# 	print(item)

	# rest = obj.get_one_from_oid('5b9f5e3c2b5c3740d095ab65')
	# print(rest)

	# rest = obj.update()
	# print(rest.matched_count)
	# print(rest.modified_count)

	# rest = obj.delete()
	# print(rest.deleted_count)


if __name__ == '__main__':
	main()