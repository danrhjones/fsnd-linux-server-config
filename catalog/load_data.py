import json

from database_setup import Item, Category
from db_helper import db_session

session = db_session()

with open('test_data.json') as data_file:
    data = json.load(data_file)

for catIndex, categories in enumerate(data, start=0):
    session.add(Category(name = categories['catagory_name']))
    for index, itemsIndex in enumerate(categories['items'], start=0):
        item = Item(category_id = catIndex + 1,
                     title = data[catIndex]['items'][index]['title'],
                     description = data[catIndex]['items'][index]['description'],
                     filename = data[catIndex]['items'][index]['filename'])
        session.add(item)
        session.commit()
