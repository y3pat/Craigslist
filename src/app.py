from fastapi import FastAPI, Query, Depends
from typing import Optional, List
from sqlalchemy import create_engine, Column, String, Float, Text, REAL
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import func
import json

Base = declarative_base()
app = FastAPI()

with open('../data/item_data.json', 'r') as f:
    data = json.load(f)

class Items(Base):
    __tablename__ = "itemdata"
    id = Column(Text, primary_key=True, index=True)
    lat = Column(REAL, index=True)
    long = Column(REAL)
    userId = Column(Text)
    description = Column(String, nullable=True)
    price = Column(Float, index=True)
    status = Column(String)


db_url = "sqlite:///./database.db"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
# will only need to do this for the last one since don't need to convert
# for the getting items with specified location

def insert_item_values(session, data):
    for item in data:
        itemLoc = list(item['loc'])
        id = item['id']
        long = itemLoc[0]
        lat = itemLoc[1]
        userId = item['userId']
        desc = item['description']
        price = item['price']
        status = item['status']
        final_item = {'id': id,
                      'lat': lat,
                      'long': long,
                      'userId': userId,
                      'description': desc,
                      'price': price,
                      'status': status
                      }
        item_values = Items(**final_item)
        session.add(item_values)
    session.commit()

session = Session()
insert_item_values(session, data)
session.close()
#
# //psuedo code
# fetch from dbm
# for
#     loc = [db.lag, db.long]
#

output_format = {'id': '',
                 'loc': [0.0, 0.0],
                 'userId': '',
                 'description': '',
                 'price': 0.0,
                 'status': ''
                 }

def format_all(all_items):
    output_lst = []
    for i in range(len(all_items)):
        item = all_items[i]
        dictionaries = {}
        dictionaries['id'] = item.id
        dictionaries['loc'] = [item.long, item.lat]
        dictionaries['userId'] = item.userId
        dictionaries['description'] = item.description
        dictionaries['price'] = item.price
        dictionaries['status'] = item.status
        output_lst.append(dictionaries)

    return output_lst
@app.get("/")
def get_data(db: session=Depends(get_db)):
    output = db.query(Items).all()
    return format_all(output)



@app.get("/getsorteddata")
def data_sortedby_price(db: session = Depends(get_db),
                        reverse: Optional[bool]=True,
                        criteria: Optional[str]='price'):
    criteria_dict = {
        'price': Items.price,
        'loc': Items.long,
        'userId': Items.userId,
        'id': Items.id,
        'description': Items.description,
        'status': Items.status
    }
    if reverse:
        query = db.query(Items).order_by(None).order_by(criteria_dict[criteria].desc())
    else:
        query = db.query(Items).order_by(None).order_by(criteria_dict[criteria].asc())
    return format_all(query.all())

@app.get("/getitem")
def getitem(db: session = Depends(get_db), id: Optional[str] = None,
            location: Optional[List[float]] = Query(None)):
    if id != None:
        output = db.query(Items).where(Items.id == id).all()
        if len(output) == 0:
            return "There is no listing with that id."
        return format_all(output)

    if location != None:
        long = location[0]
        lat = location[1]
        output = db.query(Items).where(Items.long == long,
                                       Items.lat == lat).all()
        if len(output) == 0:
            return "There is no listing with that location."
        return format_all(output)

    return "No parameters given."

@app.get("/getitemslist")
def getitemslist(db: session = Depends(get_db), status: Optional[str] = None,
                 userid: Optional[str] = None):
    if status:
        output = db.query(Items).where(Items.status == status).all()
        if len(output) == 0:
            return "There are no items listed with that status."
        return format_all(output)

    if userid:
        output = db.query(Items).where(Items.userId == userid).all()
        if len(output) == 0:
            return "There are no items listed by a user with that id."
        return format_all(output)

    return f"No parameters given."
#
@app.get("/get items in radius")
def get_items_in_radius(db: session = Depends(get_db),
                        radius: Optional[int] = 0,
                        longitude: Optional[int] = 100,
                        latitude: Optional[int] = 100):
    output = db.query(Items).filter(func.sqrt(
                                                func.pow((Items.long-longitude), 2) +
                                                func.pow((Items.lat-latitude), 2)
                                             ) <= radius
                                    ).all()
    if len(output) == 0:
        return "No items listed have a location within that radius."

    return format_all(output)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10001)
