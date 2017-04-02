import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items = []
class Item(Resource):
    parser = reqparse.RequestParser()
    # only pass the price argument
    parser.add_argument('price', type=float, required=True, help="This filed cannnot be left blank")

    @staticmethod
    def get_item_by_name(name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {'item': {'name': row[0], 'price' :row[1]}}

    @jwt_required() # authenticate before call get method, here we need the JWT to call get method
    def get(self, name):
        item = Item.get_item_by_name(name)
        if item:
            return item
        return {'msg': 'item not found'}, 404

    def post(self, name):
        if Item.get_item_by_name(name):
            return {'msg': "AN item with name '{}' already exists".format(name)}, 400 #bad request
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'msg': 'An error occurred inserting the item'}, 500#internal server error
        return item, 201 # 201 created, 202 accepted

    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price'], ))
        conn.commit()
        conn.close()

    def delete(self, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name, ))
        conn.commit()
        conn.close()
        return {'msg': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        item = Item.get_item_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'msg': 'An error occurred inserting'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'msg': 'An error occureed when updating item'}, 500
        return updated_item # show to the browser

    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name'], ))
        conn.commit()
        conn.close()

class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall() # return a list of lists
        conn.commit()
        conn.close()
        items = []
        for row in rows:
            items.append({'name': row[0], 'price': row[1]})
        return {'items': items}
