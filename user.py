import sqlite3
from flask_restful import Resource, reqparse


class User:

    def __init__(self, _id, username, email, password):
        self.id = _id # id python keyword so underscore
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,)) # create tuple with brackets (,) and comma after item - tuple needed in query
        row = result.fetchone()
        if row:
            user = cls(*row) # expands row, same as row[0], row[1], row[2]
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def find_by_email(cls, email):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE email=?"
        result = cursor.execute(query, (email,)) # create tuple with brackets (,) and comma after item - tuple needed in query
        row = result.fetchone()
        if row:
            user = cls(*row) # expands row, same as row[0], row[1], row[2]
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,)) # create tuple with brackets (,) and comma after item - tuple needed in query
        row = result.fetchone()
        if row:
            user = cls(*row) # expands row, same as row[0], row[1], row[2]
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('email',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return({"message": "A User with that name already exists."})

        if User.find_by_email(data['email']):
            return({"message": "A User with that email already exists."})    

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?, ?)"
        cursor.execute(query, (data['username'], data['email'], data['password']))

        connection.commit()
        connection.close()

        return({"message": "User created successfully."}), 201
