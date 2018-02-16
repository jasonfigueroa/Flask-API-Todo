from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="A username is required to register."
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="A password is required to register."
	)
	def post(self):
		data = UserRegister.parser.parse_args()
		
		if UserModel.find_by_username(data['username']):
			return {"message": "User with that name already exists."}
		
		user = UserModel(data['username'], data['password'])
		user.save_to_db()
		return {"message": "User created successfully."}, 201

