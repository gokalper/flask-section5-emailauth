from werkzeug.security import safe_str_cmp #safer way of comparing strings, unicode 8 ascii issues
from user import User
import sys

# def authenticate(username, password):
#     user = User.find_by_username(username)
#     if user and safe_str_cmp(user.password, password):
#         return user

def authenticate(email, password):
    print("user.username", file=sys.stderr)

    user = User.find_by_email(email)
    print("user.username", file=sys.stderr)
    if user and safe_str_cmp(user.password, password):
        print(user.email, file=sys.stderr)
        return user

def identity(payload):      #jwt specific, payload is the token
    user_id = payload['identity']
    return User.find_by_id(user_id)
