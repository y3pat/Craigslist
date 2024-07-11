from fastapi import FastAPI, Query, Depends
from src.Controller import ItemsController
from typing import Optional, List
from src.utils import format_items, check_boolean, criteria_dict
from database_sessions import Session, get_db

app = FastAPI()

session = Session()
session.close()

# Before beginning, if using the json attached must put "alembic upgrade +1"
# or "alembic upgrade head" into the terminal to create the item data table.

# Then, you must put (assume "" quotations just mean command that is inputted
# but '' means actual quotes to input in command)
# "python -m 'migrations.insert_itemdata'"

# all of this must be performed in directory Craigslist

@app.get('/')
def server_online():
    return {'status': True}

@app.get('/alldata')
def show_all_data(db: session = Depends(get_db)):
    controller = ItemsController(db)
    return format_items(controller.all_data())


@app.get('/getsorteddata')
async def get_sorted_data(db: session = Depends(get_db),
                    reverse: Optional[str] = 'true',
                    criteria: Optional[str] = 'price'):
    try:
        criteria_test = criteria_dict[criteria]
    except KeyError:
        return "That is not a valid criteria."
    reverse = check_boolean(reverse)

    controller = ItemsController(db)
    if reverse[1] == 1:
        return format_items(
            controller.get_items_sorted(reverse[0], criteria_dict[criteria]))
    else:
        return 'Reverse must be a valid boolean value.'


@app.get('/getitem')
async def getitem(db: session = Depends(get_db),
            id: Optional[str] = None,
            location: Optional[List[float]] = Query(None)):
    controller = ItemsController(db)

    if id != None and location != None:
        return format_items(controller.item_by_id_and_location(id, location))

    if id != None:
        return format_items(controller.item_by_id(id))

    if location != None:
        return format_items(controller.item_by_location(location))

    return "No id or location parameters were given."


@app.get('/getitemslist')
async def getitemslist(db: session = Depends(get_db), status: Optional[str] = None,
                 userid: Optional[str] = None):
    controller = ItemsController(db)

    if status and userid:
        output = controller.items_list_by_status_and_userId(status, userid)
        if len(output) == 0:
            return "There are not items listed with that status and userId."
        return format_items(output)

    if status:
        output = controller.items_list_by_status(status)
        if len(output) == 0:
            return "There are no items listed with that status."
        return format_items(output)

    if userid:
        output = controller.items_list_by_userId(userid)
        if len(output) == 0:
            return "There are no items listed by a user with that id."
        return format_items(output)

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

    return format_items(output)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10001)
