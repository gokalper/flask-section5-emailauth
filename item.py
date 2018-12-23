from flask_restful import Resource, reqparse
# from flask import request
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:
            return ({"item": {"name": row[0], "price": row[1]}})

    
    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query,(item['name'],item['price']))
        
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))
        
        connection.commit()
        connection.close()        

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            return item
        return({'message': "Item not found"}), 404
    
    @jwt_required()
    def post(self, name):

        if Item.find_by_name(name):
            return({'message': "An item with name '{}' already exists.".format(name)}), 400
        
        data = Item.parser.parse_args()
        item = {"name": name, "price": data['price']}

        try:
            self.insert(item)
        except:
            return {"message": "An error occured inserting the item."}, 500 #internal server error

        return (item), 201   #created vs accepted 202 - postpones creation

    @jwt_required()
    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        if row:        
            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            return({'message': 'Item Deleted'}), 202 #deleted
            
        
        connection.close()
        return({'message': 'Item not found'}), 404

    @jwt_required()
    def put(self,name):
        data = Item.parser.parse_args()

        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occured inserting item."}, 500
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occured updating item."}, 500

        return updated_item

class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return({'items': items})
