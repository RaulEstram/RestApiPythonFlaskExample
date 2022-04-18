from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.store import StoreModel
from schemas.store import StoreSchema
from libs.strings import gettext

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {"message": gettext("store_not_found")}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": gettext("store_name_exists").format(name)}
        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except Exception:
            return {"messsage": gettext("store_error_inserting")}
        return store_schema.dump(store), 201

    @jwt_required()
    def put(self, name):
        data = request.get_json()
        store = StoreModel.find_by_name(name)
        if store is None:
            store = StoreModel(**data)
        else:
            store.name = data["name"]
        store.save_to_db()
        return store_schema.dump(store)

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": gettext("store_deleted")}, 200
        return {"message": gettext("store_not_found")}, 404


class StoresList(Resource):

    @jwt_required()
    def get(self):
        stores = store_list_schema.dump(StoreModel.find_all())
        return {"Stores": stores}, 200
