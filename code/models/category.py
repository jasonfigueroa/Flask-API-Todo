from db import db

class CategoryModel(db.Model):
	__tablename__ = 'categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	user = db.relationship('UserModel')

	# the following is a list of tasks
	tasks = db.relationship('TaskModel', lazy='dynamic')

	def __init__(self, name, user_id):
		self.name = name
		self.user_id = user_id

	def json(self):
		return {'id': self.id, 'user_id': self.user_id, 'name': self.name, 'tasks': [task.json() for task in self.tasks.all()]}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

