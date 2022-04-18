from db import db
from typing import List


class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")

    @classmethod
    def find_by_name(cls, name):
        # cls.query.all() # select * from cls
        return cls.query.filter_by(name=name).first()  # select * from items where name=name limit 1

    def save_to_db(self):
        db.session.add(self)  # insert and update
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)  # delete
        db.session.commit()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()
