from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.category import Category, CategoryList
from resources.task import Task, TaskList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test' # omit this line if publishing this source code to a 
						# public location
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(UserRegister, '/register')
api.add_resource(Category, '/category', '/category/<_id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(Task, '/task', '/task/<_id>')
api.add_resource(TaskList, '/tasks')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(debug=True)