from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app= Flask(__name__)
app.secret_key = 'qingyun'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    # only pass the price argument
    parser.add_argument('price', type=float, required=True, help="This filed cannnot be left blank")

    @jwt_required() # authenticate before call get method, here we need the JWT to call get method
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return {'item': item}, 200
        return {'item': None}, 404

    def post(self, name):
        if len((filter(lambda x: x['name'] == name, items))) > 0:
            return {'msg': "An time with '{}' already exists.".format(name)}, 400 # bad request

        data = request.get_json(force=True) # like json.loads, get a dic
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # 201 created, 202 accepted

    def delete(self, name):
        # claim global so we can reach the items list defined outside the func
        global items
        items = filter(lambda x: x['name'] != name, items)
        return {'msg': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        # filter returns list, iter() make it iterable
        item = next(iter(filter(lambda x: x['name'] == name, items)), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)
