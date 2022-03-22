from ma import ma
from models.store import StoreModel
from models.item import ItemModel


class ItemSchama(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
