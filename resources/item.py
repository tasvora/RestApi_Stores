
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=float,
        required=True,
        help="Every item needs a store id."
    )    

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 #Error occured with the request

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json(), 201



    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
           item.delete_from_db()

           return {'message': 'Item deleted'}
        return {'message': 'Item not found'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            # item.store_id = data['store_id']
        item.save_to_db()

        return item.json()



class ItemList(Resource):
    def get(self):
        #with List comprehension
        return {'items': [item.json() for item in ItemModel.query.all()] }
        #without List comprehension
        # items = ItemModel.query.all()
        # listItem = []
        # for item in items:
        #     listItem.append(item.json())
        # return {'items': listItem}