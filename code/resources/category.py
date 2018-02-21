from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.category import CategoryModel

class Category(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type=str,
		required=True,
		help="A name must be provided to crete a category"
	)

	@jwt_required()
	def get(self, _id):
		category = CategoryModel.find_by_id(_id)
		if category and current_identity.id != category.user_id:
			return {"message": "Not authorized to view this content"}
		if category:
			return category.json()
		return {"message": "Category was not found."}, 404

	@jwt_required()
	def post(self):
		data = Category.parser.parse_args()

		name = data['name']

		category = CategoryModel.find_by_name(name)

		if category:
			return {"message": "That category, {}, already exists.".format(name)}, 400

		category = CategoryModel(name, current_identity.id)

		try:
			category.save_to_db()
		except:
			return {"message": "An error occured while creating the category."}, 500

		return category.json(), 201

	@jwt_required()
	def delete(self, _id):
		category = CategoryModel.find_by_id(_id)
		if category and current_identity.id != category.user_id:
			return {"message": "Not authorized to delete this content"}
		if category:
			category.delete_from_db()
			return {"message": "Category deleted."}
		return {"message": "Category with id {}, was not found".format(_id)}

class CategoryList(Resource):
	@jwt_required()
	def get(self):
		user_categories = [category.json() if category.user_id == current_identity.id else '' for category in CategoryModel.query.all()]
		if user_categories[0] == '' and user_categories[1] == '' and user_categories[2] == '':
			return {"message": "Active user has no registered categories"}
		return {"categories": user_categories}