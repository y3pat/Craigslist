This is a project assignment that is a representation of my learned knowledge on FastAPI and SQLAlchemy.

It involves creating an API to obtain information from a database containing an id, location, userId, description, price, and status for items listed by people for sale on Craigslist.


The following is only in relation to the sample dataset used:

The id represents the id of the listing and is unique. It is a string involving numbers and letters.
The location represents the coordinates of the user that listed the purchase. It is stored as a string of list of floats so that sqllite can handle it.
The userId is the id unique to the user that listed the purchase. There can be multiple userIds in the database. It is a string involving numbers and letters.
The description is a description of the item/sale and does not need to be filled. It can be null. It is a string.
The price is the price the item was listed at. If there is no price, the number is -1. It is a float.
The status of items can be either "tos" or "removed". It is a string.

The possible searches for the API are as follows:
getsorteddata?reverse=True&criteria=price - The items will be ordered by the criteria. If reverse is True then it is in descending order and ascending order if False. The default is False. 
Default criteria is price.

getitem?id=AAsm - This obtains the item with the specified id
getitem?location=AAsm - This obtains the item with the specified location. Since locations are in lists then it will be specified through getitem?location=x&location=y

getitemslist?status=AAsm - obtains list of items with specified status
getitemslist?userid=AAsm - obtains list of items listed by specified userId

get_items_in_radius?radius=xy&latitude=xx&longitude=yy - returns array of all items listed in the location by coordinate.

## FOR THE FOLLOWING:
 (assume " " quotations just represent the command that is inputted into the terminal but ' ' means quotes to input in the command)

#### Before beginning, if you plan on using the json attached you must put "alembic upgrade +1"
#### or "alembic upgrade head" into the terminal to create the item data table. This


#### Then, you must put "python -m 'migrations.insert_itemdata'"

#### all of this is assuming commands are performed in Craigslist directory