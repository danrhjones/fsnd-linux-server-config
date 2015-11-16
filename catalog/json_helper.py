from flask import jsonify

from db_helper import get_categories, get_all_items_by_category_id


def get_json():
    items_and_categories = serialize_categories_items()
    return jsonify(Category=[items_and_categories])

def serialize_categories_items():
    categories = get_categories()
    serializedCategories = []
    for category in categories:
        new_cat = category.serialize
        items = get_all_items_by_category_id(category.id)
        serializedItems = []
        for j in items:
            serializedItems.append(j.serialize)
        new_cat['Item'] = serializedItems
        serializedCategories.append(new_cat)
    return serializedCategories