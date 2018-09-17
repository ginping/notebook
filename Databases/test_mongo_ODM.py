from mongoengine import *

connect('school')


SEX_CHOICES = (
	('male', '男'),
	('female', '女')
)


class Grade(EmbeddedDocument):
	''' 学生的成绩 '''
	name = StringField(required=True)
	score = FloatField(required=True)


class Student(Document):
	name = StringField(max_length=32, required=True)
	nickname = StringField()
	in_time = StringField()
	age = IntField(required=True)
	sex = StringField(choices=SEX_CHOICES, required=True)
	grade = FloatField()
	grades = ListField(EmbeddedDocumentField(Grade))
	remark = StringField()

	# 元数据  指定集合和排序方式
	# meta = {
	# 	'collection': 'students',
	# 	'ordering': ['-age']
	# }


class TestMongoEngine(object):

	def add_one(self):
		''' 添加一条数据到数据库 '''
		yuwen = Grade(
			name='语文',
			score=92)
		shuxue = Grade(
			name='数学',
			score=90)
		stu_obj = Student(
			name='赵敏',
			age = 88,
			sex='female',
			grades=[yuwen, shuxue])
		stu_obj.remark = 'remark'  # 添加单条记录
		stu_obj.save()
		return stu_obj

	def get_one(self):
		''' 查询一条数据 '''
		return Student.objects.first()

	def get_more(self):
		''' 查询多条数据 '''
		return Student.objects.all()

	def get_from_oid(self, oid):
		''' 根据ID来获取数据 '''
		return Student.objects.filter(pk=oid).first()

	def update(self):
		''' 修改数据 '''
		# 修改一条数据
		# rest = Student.objects.filter(sex='male').update_one(inc__age=1)
		# return rest
		# 修改多条数据
		rest = Student.objects.filter(sex='male').update(inc__age=2)
		return rest

	def delete(self):
		''' 删除数据 '''
		# 删除一条数据
		return Student.objects.filter(sex='male').first().delete()
		# 删除多条数据
		# return Student.objects.filter(sex='male').delete()


# delete_id: 5b9f74612b5c373ce886fca5
def main():
	obj = TestMongoEngine()
	# rest = obj.add_one()
	# print(rest.id)

	# rest = obj.get_one()
	# print(rest.id)
	# print(rest.name)

	# rows = obj.get_more()
	# for row in rows:
	# 	print(row.name)

	# rest = obj.get_from_oid('5b9f74612b5c373ce886fca5')
	# if rest:
	# 	print(rest.id)
	# 	print(rest.name)

	# rest = obj.update()
	# print(rest)

	# rest = obj.delete()


if __name__ == '__main__':
	main()