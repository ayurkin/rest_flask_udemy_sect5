from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identify
app = Flask(__name__)
api = Api(app)
app.secret_key = 'alex'

jwt = JWT(app, authenticate, identify)


items = []


class ItemList(Resource):

    def get(self):
        return {'items': items}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="This field cannot be left blank!")


    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404


    def post(self, name):


        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name'{}' already exists".format(name)}, 400

        # data = request.get_json(force=True)
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price', type=float, required=True,
        #                     help="This field cannot be left blank!")
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data) #dangerous
        return item


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug=True)