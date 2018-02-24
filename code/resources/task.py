from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.task import TaskModel
from models.category import CategoryModel

class Task(Resource):
	parser = reqparse.RequestParser()
	
	parser.add_argument('title',
		type=str,
		required=True,
		help="A title is required"
	)

	parser.add_argument('category_name',
		type=str,
		required=True,
		help="A category name is required"
	)

	parser.add_argument('complete',
		type=bool,
		required=False
	)

	@jwt_required()
	def get(self, _id):
		task = TaskModel.find_by_id(_id, current_identity.id)
		if task and current_identity.id != task.user_id:
			return {"message": "Not authorized to view this content"}, 401
		if task:
			return task.json()
		return {"message": "Task not found."}, 404

	@jwt_required()
	def post(self):
		data = Task.parser.parse_args()
		
		title = data['title']
		category_name = data['category_name']

		task = TaskModel.find_by_title(title, current_identity.id)
		if task:
			return {"message": "Task '{}', already exists.".format(title)}, 400
		
		category = CategoryModel.find_by_name(category_name)

		task = TaskModel(title, current_identity.id, category.id)
		
		try:
			task.save_to_db()
		except:
			return {"message": "An error occurred while storing the task."}, 500

		return task.json(), 201

	@jwt_required()
	def put(self, _id):
		data = Task.parser.parse_args()
		
		# title = data['title']
		# category_name = data['category_name']
		complete = data['complete']

		task = TaskModel.find_by_id(_id, current_identity.id)
		if task is None:
			return {"message": "Task with id '{}', does not exist.".format(title)}, 400
		
		# category = CategoryModel.find_by_name(category_name)

		# task = TaskModel(title, current_identity.id, category.id)
		task.complete = complete
		
		try:
			task.save_to_db()
		except:
			return {"message": "An error occurred while storing the task."}, 500

		return task.json()

	@jwt_required()
	def delete(self, _id):
		task = TaskModel.find_by_id(_id)
		if task and current_identity.id != task.user_id:
			return {"message": "Not authorized to delete this content"}, 401
		if task:
			task.delete_from_db()
			return {"message": "Task deleted."}
		return {"message": "Task with id {}, was not found".format(_id)}, 404

class TaskList(Resource):
	@jwt_required()
	def get(self):
		user_tasks = [task.json() if task.user_id == current_identity.id else '' for task in TaskModel.query.all()]

		if len(user_tasks) < 1:
			return {"message": "The database currently has no tasks for any users"}, 400

		if user_tasks[0] == '':
			return {"message": "Active user has not registered any tasks"}, 404

		return {"tasks": user_tasks}
