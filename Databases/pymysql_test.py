import pymysql


class MysqlSearch(object):

	def __init__(self):
		self.get_conn()
	
	def get_conn(self):
		""" 获取连接 """
		try:
			self.conn = pymysql.connect(
				host='localhost',
				port=3306,
				user='root',
				passwd='142857',
				db='news',
				charset='utf8')
		except Exception as e:
			print('Error:%s' %e)

	def close_conn(self):
		try:
			# 关闭连接
			# if self.cur:
			# 	cur.close()
			if self.conn:
				self.conn.close()
		except Exception as e:
			print('Error: %s' %e)

	def get_one(self):
		# 准备SQL
		sql = 'SELECT * FROM news;'
		# 找到cursor
		cursor = self.conn.cursor()
		# 执行SQL
		cursor.execute(sql)
		# print(dir(cursor))
		# print(cursor.description)
		# 拿到结果
		data = cursor.fetchone()
		# print(data)
		data = dict(zip([k[0] for k in cursor.description], data))
		# 处理数据
		# print(data)
		# print(data['title'])
		# 关闭cursor/连接
		cursor.close()
		self.close_conn()
		return data

	def get_more(self, page, page_size):
		# 准备SQL
		offset = (page - 1) * page_size
		sql = f'SELECT * FROM news ORDER BY id LIMIT {offset}, {page_size};'
		# 找到cursor
		cursor = self.conn.cursor()
		# 执行SQL
		cursor.execute(sql)
		# print(dir(cursor))
		# print(cursor.description)
		# 拿到结果
		data = cursor.fetchall()
		# print(data)
		data = [dict(zip([k[0] for k in cursor.description], row)) for row in data]
		# 处理数据
		# print(data)
		# print(data['title'])
		# 关闭cursor/连接
		cursor.close()
		self.close_conn()
		return data

	def add_one(self):
		try:
		    # 准备SQL
			sql = (
				"""
				INSERT INTO news(title, image, content, types, created_at, is_valid) VALUE
	            (%s, %s, %s, %s, NOW(), %s);
	            """
				)
			# 准备连接和cursor
			cursor = self.conn.cursor()
			# 执行SQL
			cursor.execute(sql, ('标题1', 'image_url', '新闻内容', '类型', 1))
			cursor.execute(sql, ('标题3', 'image_url', '新闻内容', '类型', 0))
			# 提交数据到数据库
			# 提交事务
			self.conn.commit()
			# 关闭cursor和连接
			cursor.close()
		except Exception as e:
			print("Error: %s" %e)
			self.conn.rollback()  # 一条错误都不成功
		self.close_conn()

	def delete_one(self):
		try:
			# 准备SQL
			sql = (
				"""
				DELETE FROM news WHERE title='标题';
				"""
				)
			# 准备连接和cursor
			cursor = self.conn.cursor()
			# 执行SQL
			cursor.execute(sql)
 			# 提交事务
			self.conn.commit()
			# 关闭cursor和连接
			cursor.close()
		except Exception as e:
			print("Error: %s" %e)
			self.conn.rollback()
		self.close_conn()



def main():
	obj = MysqlSearch()
	# data = obj.get_one()
	# print(data)

	# obj.add_one()

	# obj.delete_one()

	data = obj.get_more(1, 20)
	for item in data:
		print('\n', item)


if __name__ == '__main__':
	main()

