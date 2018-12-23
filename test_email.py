import sqlite3
# from flask_restful import Resource, reqparse

class User:

    def __init__(self, _id, username, email, password):
        self.id = _id # id python keyword so underscore
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def find_by_email(cls, email):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "SELECT * FROM users WHERE email=?"
            result = cursor.execute(query, (email,)) # create tuple with brackets (,) and comma after item - tuple needed in query
            row = result.fetchone()
            if row:
                print(row)
                user = cls(*row)# expands row, same as row[0], row[1], row[2]
            else:
                user = None
            
            connection.close()
            return user

joe = User.find_by_email("joeatdomain")
print(joe.email)