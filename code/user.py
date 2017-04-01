import sqlite3

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
