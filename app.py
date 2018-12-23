from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList
import datetime

app = Flask(__name__)
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'username'
jwt = JWT(app, authenticate, identity) #jwt creates endpoint /auth

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'user_id': identity.id
                   })

# does not work...
# @jwt.error_handler
# def customized_error_handler(error):
#     return jsonify({
#                        'message': error.description,
#                        'code': error.status_code
#                    }), error.status_code

api.add_resource(Item, '/item/<string:name>')  
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':      #prevent importing this item if importing file app.py
    app.secret_key = 'jose'
    app.run(port=5000, debug=True)