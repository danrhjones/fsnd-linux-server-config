import os
import random
import string

from flask import Flask, render_template, redirect, url_for, flash
from werkzeug import secure_filename
from flask import session as login_session, request
from flask import Response
from flask.ext.seasurf import SeaSurf

from db_helper import *
from google_connect_oauth import connect_to_google, disconnect_from_google
from json_helper import get_json
from login_decorator import login_required
from xml_helper import xml_creator

app = Flask(__name__)
csrf = SeaSurf(app)
session = db_session()

# Folder to upload images to
UPLOAD_FOLDER = './static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# image extensions allowed. Any thing else will be rejected.
ALLOWED_EXTENSIONS = set(['JPG', 'jpg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/login')
def showLogin():

    """ displays the login page """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/')
@app.route('/catalog/')
def homepage():
    """
    Returns the homepage with a list of categories and the lastest item in each category
    """
    login_status=False
    if 'username' in login_session:
        login_status=True
    return render_template('index.html', wholeCatalog=wholecatalog(),
                           items=get_latest_items(), login_status=login_status)


@app.route('/catalog/<string:catalog_name>/items/')
def display_all_items_per_category(catalog_name):
    """
    Returns a page that lists all of the items in the selected category
    argument: catalog_name: a string that matches a category name in the category table
    """
    login_status=False

    if 'username' in login_session:
        login_status=True

    return render_template('catalog_items.html', wholecatalog=wholecatalog(), items=get_items_by_category(catalog_name),
                           catalog_name=catalog_name, login_status=login_status)


@app.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def add_new_catalog():

    """
    Returns a page that allows a new category to be added to the database.
    Requires the user to be logged in
    """
    if request.method == 'POST':
        session.add(Category(name =request.form.get('title')))
        session.commit()
        return homepage()

    else:
        return render_template('new_catalog.html')


@app.route('/catalog/<string:catalog_name>/new_item', methods=['GET', 'POST'])
@login_required
def add_new_item(catalog_name):
    """
    Returns a page that allows a new item to be added to a category.
    Requires the user to be logged in
    """
    if request.method == 'POST':
        catId = get_catalogId_by_catalog_name(catalog_name)
        newItem = Item(category_id = catId.id,
                       title = request.form.get('title'),
                       description = request.form.get('description'),
                       filename = request.form.get('file'))
        file = request.files['file']
        if file and allowed_file(file.filename):
            print "allowed"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            newItem.filename = file.filename

        if file and not allowed_file(file.filename):
            flash("Only jpg's are accepted")

        session.add(newItem)
        session.commit()

        item = get_item_by_item_title(request.form.get('title'))
        return redirect(url_for('display_item_description', catalog_name=catalog_name,
                                item_id=item.id))

    else:
        return render_template('new_item.html', catalog_name=catalog_name)


@app.route('/catalog/<string:catalog_name>/<int:item_id>/')
def display_item_description(catalog_name, item_id):
    """
    Returns the title, description and image of an item
    :argument catalog_name:  a string that matches a category name in the category table
    :argument item_id: an int that matches an item id in the item table
    """
    item = get_item_by_item_id(item_id)
    login_status=False

    if 'username' in login_session:
        login_status=True

    return render_template('item.html', item=get_item_by_id(catalog_name, item_id), image=item.filename,
                           item_title=item.title, login_status=login_status)


@app.route('/catalog/<int:item_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    """
    Returns a page that allows a user to edit an item
    Requires the user to be logged in
    :param item_id: an int that matches an item id in the item table
    """
    item_to_update = get_item_by_item_id(item_id)
    # print item_to_update.title
    print item_to_update.category_id

    # print type('username')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            print "allowed"
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item_to_update.filename = file.filename

        if file and not allowed_file(file.filename):
            flash("Only jpg's are accepted")

        if request.form.get('title') != '':
            item_to_update.title = request.form.get('title')

        if request.form.get('description') != '':
            item_to_update.description = request.form.get('description')

        if request.form.get('categories') != '':
            item_to_update.category_id = request.form.get('categories')

        session.add(item_to_update)
        session.commit()

        catalog_name = get_catalog_name_by_catalog_id(item_to_update.category_id)

        return redirect(url_for('display_item_description', catalog_name=catalog_name.name,
                                item_id=item_to_update.id))

    else:
        return render_template('edit.html', item_to_update=item_to_update, option_list=option_list())


@app.route('/catalog/<int:item_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    """
    Returns a page that allows a user to delete an item
    Requires the user to be logged in
    :param item_id: an int that matches an item id in the item table
    """
    item = get_item_by_item_id(item_id)

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        catalog_name = get_catalog_name_by_catalog_id(item.category_id)
        return redirect(url_for('display_all_items_per_category', catalog_name=catalog_name.name))
    else:
        return render_template('delete.html', item=item)

@app.route('/catalog.json')
def catalog_json():
    """
    Returns all of the categories and its associated items in json form
    """
    return get_json()


@app.route('/catalog.xml')
def catalog_xml():
    """
    Returns all of the categories and its associated items in XML form
    """
    return Response(xml_creator(), mimetype='application/xml')

@csrf.exempt
@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    This method is called to allow google oath sign in
    """
    return connect_to_google()

@app.route('/gdisconnect')
def gdisconnect():
    """
    logs the user out of google oauth sign in
    :return:
    """
    return disconnect_from_google()


app.secret_key = 'a secretkey'
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':
    app.debug = True
    app.secret_key ='this is my secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
