# forms.py

from wtforms import Form, StringField, SelectField, validators


class SearchForm(Form):
    choices = [('Date_to_purchase', 'Date To Purchase'),
               ('Store', 'Store Name'),
               ('Item', 'Item')
               ]
    select = SelectField('', choices=choices)
    search = StringField('')


class StoreForm(Form):

    item = StringField('Item')
    price = StringField('Price')
    quantity = StringField('Quantity')
    store_name = StringField('Store Name')
    address = StringField('Address')
    date_to_purchase = StringField('Date To Purchase')
    note = StringField('Note')
