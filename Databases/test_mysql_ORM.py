# ORM: Object Relational Mapping  对象关系映射
# https://www.cnblogs.com/aylin/p/5770888.html  参考这篇blog
# https://bugs.mysql.com/bug.php?id=82414  Bug report  // Warning
# Warning: (1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 481")
# result = self._query(query)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

engine = create_engine('mysql+pymysql://root:142857@localhost/news_test?charset=utf8', max_overflow=5) # max_overflow ?
Base = declarative_base()

Session = sessionmaker(bind=engine)

class News(Base):
	__tablename__ = 'news'
	id = Column(Integer, primary_key=True)
	title = Column(String(200), nullable=False)
	content = Column(String(2000), nullable=False)
	types = Column(String(10), nullable=False)
	created_at = Column(DateTime)
	image = Column(String(300), )
	author = Column(String(20), )
	view_count = Column(Integer)
	is_valid = Column(Boolean)


class OrmTest(object):

	def __init__(self):
		self.session = Session()

	def add_one(self):
		''' 添加数据 '''
		new_obj = News(
			title='ORM标题',
			content='content',
			types='技术'
			)
		new_obj2 = News(
			title='title',
			content='content',
			types='types'
			)
		self.session.add(new_obj)
		self.session.add(new_obj2)
		self.session.commit()
		return new_obj

	def get_one(self):
		''' 查询一条数据 '''
		return self.session.query(News).get(3)

	def get_more(self):
		''' 查询多条数据 '''
		return self.session.query(News).filter_by(is_valid=True)

	def update_data(self, pk):
		''' 修改数据 '''
		# 修改多条数据
		data_list = self.session.query(News).filter(News.id>3)
		# data_list = self.session.query(News).filter_by(is_valid=False)
		for item in data_list:
			item.is_valid = 1
			self.session.add(item)
		self.session.commit()
		# 修改单条数据
		# new_obj = self.session.query(News).get(pk)
		# if new_obj:
		# 	new_obj.is_valid = 0
		# 	self.session.add(new_obj)
		# 	self.session.commit()
		# 	return True
		# return False

	def delete_data(self, pk):
		''' 删除数据 '''
		# 获取要删除的数据
		new_obj = self.session.query(News).get(pk)
		if new_obj:
			self.session.delete(new_obj)
			self.session.commit()



def main():
	obj = OrmTest()
	# test = obj.add_one()
	# print(test.id)

	# test = obj.get_one()
	# if test:
	# 	print(f'ID:{test.id} => title:{test.title}')
	# else:
	# 	print('Not exist.')

	# result = obj.get_more()
	# print(result.count())
	# for new_obj in result:
	# 	print(f'ID:{new_obj.id} => title:{new_obj.title}')

	# print(obj.update_data(3))
	print(obj.delete_data(1))

if __name__ == '__main__':
	main()
