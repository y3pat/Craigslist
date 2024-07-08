from fastapi import FastAPI, Query, Depends
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from Model import Items
from Controller import ItemsController
from utils import format_all, check_boolean
app = FastAPI()

db_url = "sqlite:///./database.db"

engine = create_engine(db_url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
session = Session()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def insert_items(db: session=Depends(get_db)):
    controller = ItemsController(db)
    try:
        controller.insert_initial_values()
    except:
        return "Values could not be inserted properly"


@app.get('/')
def show_all_data(db: session=Depends(get_db)):
    controller = ItemsController(db)
    return format_all(controller.all_data())

@app.get('/getsorteddata')
def get_sorted_data(db: session=Depends(get_db),
                    reverse: Optional[str] = 'true',
                    criteria: Optional[str] = 'price'):
    criteria_dict = {
        'price': Items.price,
        'loc': Items.long,
        'userId': Items.userId,
        'id': Items.id,
        'description': Items.description,
        'status': Items.status
    }

    try:
        criteria_test = criteria_dict[criteria]
    except KeyError:
        return "That is not a valid criteria."
    reverse = check_boolean(reverse)

    controller = ItemsController(db)
    if reverse[1] == 1:
        return format_all(controller.get_items_sorted(reverse[0], criteria_dict[criteria]))
    else:
        return 'Reverse must be a valid boolean value.'

@app.get('/getitem')
def getitem(db: session=Depends(get_db),
            id: Optional[str] = None,
            location: Optional[List[float]] = Query(None)):

    controller = ItemsController(db)

    if id != None and location != None:
        return format_all(controller.item_by_id_and_location(id, location))

    if id != None:
        return format_all(controller.item_by_id(id))

    if location != None:
        return format_all(controller.item_by_location(location))

    return "No id or location parameters were given."

@app.get('/getitemslist')
def getitemslist(db: session = Depends(get_db), status: Optional[str] = None,
                 userid: Optional[str] = None):
    controller = ItemsController(db)

    if status and userid:
        output = controller.items_list_by_status_and_userId(status, userid)
        if len(output) == 0:
            return "There are not items listed with that status and userId."
        return format_all(output)

    if status:
        output = controller.items_list_by_status(status)
        if len(output) == 0:
            return "There are no items listed with that status."
        return format_all(output)

    if userid:
        output = controller.items_list_by_userId(userid)
        if len(output) == 0:
            return "There are no items listed by a user with that id."
        return format_all(output)

    return f"No parameters given."

@app.get('/get items in radius')
def get_items_in_radius(db: session = Depends(get_db),
                        radius: Optional[float] = 0.0,
                        longitude: Optional[float] = 100.0,
                        latitude: Optional[float] = 100.0):

    controller = ItemsController(db)
    output = controller.items_in_radius(radius, longitude, latitude)

    if len(output) == 0:
        return "No items listed have a location within that radius."

    return format_all(output)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10001)
