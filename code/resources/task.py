from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.task import TaskModel

class Task(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('user_id',
		type=int,
		required=True,
		help="A user id is required"
	)
	parser.add_argument('category_id',
		type=int,
		required=True,
		help="A category id is required"
	)

	@jwt_required()
	def get(self, title):
		task = TaskModel.find_by_title(title)
		if task:
			return task.json()
		return {"message": "Task not found."}

	def post(self, title):
		data = Task.parser.parse_args()
		task = TaskModel.find_by_title(title)
		if task:
			return {"message": "Task '{}', already exists."}
		task = TaskModel(title, data['user_id'], data['category_id'])
		
		try:
			task.save_to_db()
		except:
			return {"message": "An error occurred while storing the task."}

		return task.json(), 201

	def delete(self, title):
		task = TaskModel.find_by_title(title)
		if task:
			task.delete_from_db()
		return {"message": "Task deleted."}

class TaskList(Resource):
	def get(self):
		return {"tasks": [task.json() for task in TaskModel.query.all()]}
