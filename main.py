# main.py

from app import app
from db_setup import init_db, db_session
from forms import SearchForm, StoreForm
from flask import flash, render_template, request, redirect
from models import Store, Item
from tables import Results


init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    qry = db_session.query(Store)
    results = qry.order_by(Store.date_to_purchase).all()
    table = Results(results)
    table.border = True
    return render_template('index.html', form=search, table=table)


@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Item':
            qry = db_session.query(Store, Item).filter(
                Item.id==Store.item_id).filter(
                    Item.name.contains(search_string))
            results = [item[0] for item in qry.all()]
        elif search.data['select'] == 'Store':
            qry = db_session.query(Store).filter(
                Store.store_name.contains(search_string))
            results = qry.order_by(Store.date_to_purchase).all()
        elif search.data['select'] == 'Date_to_purchase':
            qry = db_session.query(Store).filter(
                Store.date_to_purchase.contains(search_string))
            results = qry.order_by(Store.date_to_purchase).all()
        else:
            qry = db_session.query(Store)
            results = qry.order_by(Store.date_to_purchase).all()
    else:
        qry = db_session.query(Store)
        results = qry.order_by(Store.date_to_purchase).all()
    if not results:
        flash('Invalid search input, no results found! Please input a valid search!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)


@app.route('/new_store', methods=['GET', 'POST'])
def new_store():
    """
    Add a new store
    """
    form = StoreForm(request.form)

    if request.method == 'POST' and form.validate():
        # save the store
        store = Store()
        save_changes(store, form, new=True)
        flash('A new record(s) has (have) been added successfully!')
        return redirect('/new_store')

    return render_template('new_store.html', form=form)


def save_changes(store, form, new=True):
    """
    Save the changes to the database
    """
    # Get data from form and assign it to the correct attributes
    # of the SQLAlchemy table object
    item = Item()
    item.name = form.item.data

    store.item = item
    store.price = form.price.data
    store.quantity = form.quantity.data
    store.store_name = form.store_name.data
    store.address = form.address.data
    store.date_to_purchase = form.date_to_purchase.data
    store.note = form.note.data

    if new:
        # Add the new store to the database
        db_session.add(store)

    # commit the data to the database
    db_session.commit()


@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Store).filter(
                Store.id==id)
    store = qry.first()

    if store:
        form = StoreForm(formdata=request.form, obj=store)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(store, form)
            flash('My shopping list has been updated successfully!')
            return redirect('/')
        return render_template('edit_store.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)


@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    """
    Delete the item in the database that matches the specified
    id in the URL
    """
    qry = db_session.query(Store).filter(
        Store.id==id)
    store = qry.first()

    if store:
        form = StoreForm(formdata=request.form, obj=store)
        if request.method == 'POST' and form.validate():
            # delete the item from the database
            db_session.delete(store)
            db_session.commit()

            flash('Record has been deleted successfully!')
            return redirect('/')
        return render_template('delete_store.html', form=form)
    else:
        return 'Error deleting #{id}'.format(id=id)


if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = True
    app.run(port=5001)
