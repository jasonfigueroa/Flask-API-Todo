from db import db
from models.category import CategoryModel

class TaskModel(db.Model):
	__tablename__ = 'tasks'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('UserModel')

	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
	category = db.relationship('CategoryModel')

	def __init__(self, title, user_id, category_id):
		self.title = title
		self.user_id = user_id
		self.category_id = category_id

	def json(self):
		category = CategoryModel.find_by_id(self.category_id)
		return {'id': self.id,'title': self.title, 'category': category.name}

	@classmethod
	def find_by_title(cls, title, user_id):
		subquery = cls.query.filter_by(title=title)
		return subquery.filter_by(user_id=user_id).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()