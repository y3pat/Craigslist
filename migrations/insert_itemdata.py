import json
from Models.itemdata_model import Items
from database_sessions import Session
import sqlalchemy

session = Session()


def insert_all_items(db: session=Session()):
    with open('data/item_data.json', 'r') as f:
        data = json.load(f)

    for item in data:
        id = item.get('id')

        try:
            itemLoc = list(item['loc'])
        except KeyError:
            itemLoc = [sqlalchemy.null(), sqlalchemy.null()]
        if len(itemLoc) == 2:
            long = itemLoc[0]
            lat = itemLoc[1]
        else:
            long = sqlalchemy.null()
            lat = sqlalchemy.null()

        userId = item.get('userId', sqlalchemy.null())
        desc = item.get('description', sqlalchemy.null())
        price = item.get('price', -1.0)
        status = item.get('status', sqlalchemy.null())

        try:
            userId = str(userId)
        except ValueError:
            userId = sqlalchemy.null()
        try:
            desc = str(desc)
        except ValueError:
            desc = sqlalchemy.null()
        try:
            price = int(price)
        except ValueError:
            price = -1.0
        try:
            status = str(status)
        except ValueError:
            status = sqlalchemy.null()

        final_item = {
            'id': id,
            'lat': lat,
            'long': long,
            'userId': userId,
            'description': desc,
            'price': price,
            'status': status
        }
        item_values = Items(**final_item)
        db.add(item_values)
    db.commit()
    db.close()
session.close()

insert_all_items()
