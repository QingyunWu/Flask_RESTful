from user import User

users = [
    User(1, 'qingyun', 'wqycfc1992'),
    User(2, 'kane', 'kane559')
]

username_mapping = {
    u.username: u for u in users
}

userid_mapping = {
    u.id: u for u in users # set comprehension
}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)


# first authenticate by username and password, then the server return a JSON Werb Token,
# use this JWT, the client's request will be sererved as it's already logged in
