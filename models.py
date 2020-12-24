from app import db


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return "{}".format(self.name)


class Store(db.Model):
    """"""
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    store_name = db.Column(db.String)
    address = db.Column(db.String)
    date_to_purchase = db.Column(db.String)
    note = db.Column(db.String(20))

    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    item = db.relationship("Item", backref=db.backref(
        "stores", order_by=id))
