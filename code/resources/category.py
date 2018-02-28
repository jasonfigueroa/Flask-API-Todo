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
			return {"message": "Not authorized to view this content"}, 401
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
			return {"message": "Not authorized to delete this content"}, 401
		if category:
			try:
				category.delete_from_db()			
			except Exception as ex:
				if type(ex) == 'IntegrityError':
					return {"message": "Please make sure you are not trying to delete a category that is still in use by an existing task."}, 400
				else:
					return {"message": "An error occurred and the request could not be completed"}, 500

			return {"message": "Category deleted."}
		return {"message": "Category with id {}, was not found".format(_id)}, 404

class CategoryList(Resource):
	@jwt_required()
	def get(self):
		user_categories = [category.json() for category in CategoryModel.query.all() if category.user_id == current_identity.id]

		# if len(user_categories) < 1:
		# 	return {"message": "The database currently has no categories for any users"}, 400
		
		# if user_categories[0] == '':
		# 	return {"message": "Active user has no registered categories"}, 404
		
		return {"categories": user_categories}