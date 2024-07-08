from sqlalchemy.orm import Session
from DAO import ItemsDAO

class ItemsController:
    def __init__(self, db: Session):
        self.dao = ItemsDAO(db)

    def insert_initial_values(self):
        self.dao.insert_all_items()

    def all_data(self):
        return self.dao.get_all_items()

    def get_items_sorted(self, reverse, criteria):
        return self.dao.sort_items(reverse, criteria)

    def item_by_id(self, id):
        return self.dao.get_item_by_id(id)

    def item_by_location(self, loc):
        return self.dao.get_item_by_location(loc)

    def item_by_id_and_location(self, id, loc):
        return self.dao.get_item_by_id_and_location(id, loc)

    def items_list_by_status(self, status):
        return self.dao.get_items_by_status(status)

    def items_list_by_userId(self, userId):
        return self.dao.get_items_by_userId(userId)

    def items_list_by_status_and_userId(self, status, userId):
        return self.dao.get_items_by_status_and_userId(status, userId)

    def items_in_radius(self, radius, longitude, latitude):
        return self.dao.get_items_in_radius(radius, longitude, latitude)