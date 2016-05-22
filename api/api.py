from flask import Flask
from flask_restful import Api
from resources.property_resource import PropertyAPI, PropertyListAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(PropertyAPI, '/properties/<int:id>')
api.add_resource(PropertyListAPI, '/properties')