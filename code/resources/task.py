from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.task import TaskModel
from models.category import CategoryModel

class Task(Resource):
	parser = reqparse.RequestParser()
	# parser.add_argument('user_id',
	# 	type=int,
	# 	required=True,
	# 	help="A user id is required"
	# )
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

	@jwt_required()
	def get(self, _id):
		task = TaskModel.find_by_id(_id)
		if task and current_identity.id != task.user_id:
			return {"message": "Not authorized to view this content"}
		if task:
			return task.json()
		return {"message": "Task not found."}
		# return {"current_identity": "{}".format(current_identity.id)}

	@jwt_required()
	def post(self):
		data = Task.parser.parse_args()
		
		title = data['title']
		category_name = data['category_name']

		task = TaskModel.find_by_title(title, current_identity.id)
		if task:
			return {"message": "Task '{}', already exists.".format(title)}
		
		category = CategoryModel.find_by_name(category_name)
		# want to programatically derive the user_id
		task = TaskModel(title, current_identity.id, category.id)
		
		try:
			task.save_to_db()
		except:
			return {"message": "An error occurred while storing the task."}

		return task.json(), 201

	def delete(self, _id):
		task = TaskModel.find_by_id(_id)
		if task:
			task.delete_from_db()
		return {"message": "Task deleted."}

class TaskList(Resource):
	def get(self):
		return {"tasks": [task.json() for task in TaskModel.query.all()]}
