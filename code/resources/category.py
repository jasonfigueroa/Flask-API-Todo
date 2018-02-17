from flask_restful import Resource, reqparse
from models.category import CategoryModel

class Category(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('name',
		type=str,
		required=True,
		help="A name must be provided to crete a category"
	)

	def get(self, _id):
		category = CategoryModel.find_by_id(_id)
		if category:
			return category.json()
		return {"message": "Category was not found."}, 404

	def post(self):
		data = Category.parser.parse_args()

		name = data['name']

		category = CategoryModel.find_by_name(name)

		if category:
			return {"message": "That category {} already exists.".format(name)}, 400

		category = CategoryModel(name)

		try:
			category.save_to_db()
		except:
			return {"message": "An error occured while creating the category."}, 500

		return category.json(), 201

	def delete(self, _id):
		category = CategoryModel.find_by_id(_id)

		if category:
			category.delete_from_db()

		return {"message": "Category deleted."}

class CategoryList(Resource):
	def get(self):
		return {"categories": [category.json() for category in CategoryModel.query.all()]}