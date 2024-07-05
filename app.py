from fastapi import FastAPI, Query, Depends
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import json

Base = declarative_base()
app = FastAPI()

with open('item_data.json', 'r') as f:
    data = json.load(f)

class Items(Base):
    __tablename__ = "itemdata"
    id = Column(Text, primary_key=True)
    loc = Column(String)
    userId = Column(Text)
    description = Column(String, nullable=True)
    price = Column(Float)
    status = Column(String)

db_url = "sqlite:///./database.db"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def serialize(loc):
    return json.dumps(loc)

def deserialize(loc):
    return json.loads(loc)

with open('data.json', 'r') as f:
    data = json.load(f)

def insert_item_values(session, data):
    for item in data:
        item['loc'] = serialize(item['loc'])
        item_values = Items(**item)
        session.add(item_values)
    session.commit()

session = Session()
insert_item_values(session, data)
session.close()

def get_data(session):
    items = session.query(Items).all()
    for item in items:
        item.loc = deserialize(item.loc)
        print(item.id, item.loc, item.userId, item.description, item.price, item.status)

def data_sortedby_price(reverse=True):
    if reverse:
        query = session.query(Items).order_by(None).order_by(Items.price.desc())
    else:
        query = session.query(Items).order_by(None).order_by(Items.price.asc())
    return query.all()

session = Session()
all_data = session.query(Items).all()

price_sorted_results = data_sortedby_price(False)
for item in price_sorted_results:
    print(f"[\nID: {item.id}, \nLocation: {item.loc}, \nUserID: {item.userId}, "
          f"\nDescription: {item.description}, \nPrice: {item.price}, \nStatus: {item.status}\n]\n")
session.close()
