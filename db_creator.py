from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///shopping_list.db', echo=True)
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Item: {}>".format(self.name)


class Store(Base):
    """"""
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True)
    item = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    store_name = Column(String)
    address = Column(String)
    date_to_purchase = Column(String)
    note = Column(String(20))

    item_id = Column(Integer, ForeignKey("items.id"))
    item = relationship("Item", backref=backref(
        "stores", order_by=id))


# create tables
Base.metadata.create_all(engine)
