from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, Category


engine = create_engine('postgresql://grader:password@localhost/itemcatalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def db_session():
    return session


def add(item):
    session.add(item)


def delete(item):
    session.delete(item)


def commit():
    session.commit()


def wholecatalog():
    return session.query(Category).all()


def get_items_by_category(catalog_name):
    return session.query(Item).join(Category).filter(Category.name == catalog_name).all()


def get_item(catalog_name, item_title):
    return session.query(Item).join(Category).filter(Category.name == catalog_name, Item.title == item_title).all()

def get_item_by_id(catalog_name, item_id):
    return session.query(Item).join(Category).filter(Category.name == catalog_name, Item.id == item_id).one()


def get_catalogId_by_catalog_name(catalog_name):
    return session.query(Category).filter(Category.name == catalog_name).one()

def get_catalog_name_by_catalog_id(catalog_id):
    return session.query(Category).filter(Category.id == catalog_id).one()


def get_all_items_by_category_id(category_id):
    return session.query(Item).filter(Item.category_id == category_id).all()


def get_categories():
    return session.query(Category).all()


def get_item_by_item_title(item_title):
    return session.query(Item).filter(Item.title == item_title).first()

def get_item_by_item_id(item_id):
    return session.query(Item).filter(Item.id == item_id).one()




def option_list():
    return session.query(Category).all()


def get_latest_items():
    return session.query(Item.title,Item.id, Category.name).distinct(Item.category_id).join(Category)
