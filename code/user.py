import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def get_by_username(cls, username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        # in cursor.execute, the parameter should be a tuple, needs comma here
        result = cursor.execute(query, (username,))
        row = result.fetchone() # row is a sequence
        if row is not None:
            user = cls(row[0], row[1], row[2])
            #user = cls(*row)
        else:
            user = None
        cursor.close()
        conn.close()
        return user
    @classmethod
    def get_by_userid(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        # in cursor.execute, the parameter should be a tuple, needs comma here
        result = cursor.execute(query, (_id,))
        row = result.fetchone() # row is a sequence
        if row is not None:
            user = cls(row[0], row[1], row[2])
            #user = cls(*row)
        else:
            user = None
        cursor.close()
        conn.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field connot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        # check the db to see if the username already exist
        if User.get_by_username(data['username']):
            return {'msg': 'user already exists'}, 400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password'], ))

        conn.commit()
        cursor.close()
        conn.close()

        return {'msg': "User created successfullly"}, 201
