from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.item import ItemModel
from schemas.item import ItemSchama
from libs.strings import gettext

item_schema = ItemSchama()
item_list_schema = ItemSchama(many=True)


class Item(Resource):

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)
        return {'message': gettext("item_not_found")}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': gettext("item_name_exists").format(name)}
        item_json = request.get_json()
        item_json["name"] = name
        item = ItemModel(**item_json)
        try:
            item.save_to_db()
        except:
            return {"message": gettext("item_error_inserting")}
        return item_schema.dump(item), 201

    @jwt_required()
    def put(self, name):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = item_json["price"]
            item.store_id = item_json["store_id"]
        else:
            item = item_schema.load(item_json)
        item.save_to_db()
        return item_schema.dump(item), 200

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": gettext("item_deleted")}, 200
        return {"message": gettext("item_not_found")}, 404


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()  # como el jwt es opcional, puede darnos el id con el que hicimos logging o un None si no realizamos un logging
        items = item_list_schema.dump(ItemModel.find_all())
        if user_id:
            return {"items": items}, 200
        return {
                   "items": [item["name"] for item in items],
                   "message": "More data available if you log in."
               }, 200
