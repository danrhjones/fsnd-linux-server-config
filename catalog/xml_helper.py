from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement

from db_helper import get_categories, get_all_items_by_category_id


def xml_creator():
    categories = get_categories()
    feed = Element('xmlFeed')

    category = SubElement(feed, 'category')
    for categories_to_output in categories:

        SubElement(category, 'category', id=str(categories_to_output.id))
        SubElement(category, 'category', name=str(categories_to_output.name))

        itemList = get_all_items_by_category_id(categories_to_output.id)
        for items_to_output in itemList:
            items = SubElement(category, 'items')

            SubElement( items, 'item', description=str(items_to_output.description))
            SubElement( items, 'item', id=str(items_to_output.id))
            SubElement( items, 'item', title=str(items_to_output.title))

    return prettify(feed)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    copied from: http://pymotw.com/2/xml/etree/ElementTree/create.html
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")



