import sqlalchemy
from sqlalchemy.orm import Session
from Model import Items
from sqlalchemy import func
import json

class ItemsDAO:
    def __init__(self, db: Session):
        self.db = db

    def insert_all_items(self):
        with open('../data/item_data.json', 'r') as f:
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
            self.db.add(item_values)
        self.db.commit()

    def get_all_items(self):
        return self.db.query(Items).all()

    def sort_items(self, reverse, criteria):
        if reverse:
            return self.db.query(Items).order_by(criteria.desc()).all()
        else:
            return self.db.query(Items).order_by(criteria.asc()).all()

    def get_item_by_id(self, id):
        return self.db.query(Items).where(Items.id == id).all()

    def get_item_by_location(self, loc):
        long = loc[0]
        lat = loc[1]
        return self.db.query(Items).where(Items.long == long, Items.lat == lat).all()

    def get_item_by_id_and_location(self, id, loc):
        long = loc[0]
        lat = loc[1]
        return self.db.query(Items).where(Items.id == id, Items.long == long, Items.lat == lat).all()

    def get_items_by_status(self, status):
        return self.db.query(Items).where(Items.status == status).all()

    def get_items_by_userId(self, userId):
        return self.db.query(Items).where(Items.userId == userId).all()

    def get_items_by_status_and_userId(self, status, userId):
        return self.db.query(Items).where(Items.status == status, Items.userId == userId).all()

    def get_items_in_radius(self, radius, longitude, latitude):
        # noinspection PyTypeChecker
        return self.db.query(Items).filter(func.sqrt(
                                                func.pow(
                                                    func.coalesce(Items.long-longitude, 0), 2
                                                ) +
                                                func.pow(
                                                    func.coalesce(Items.lat-latitude, 0), 2
                                                )
                                             ) <= radius
                                    ).all()

