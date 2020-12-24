from flask_table import Table, Col, LinkCol


class Results(Table):
    id = Col('Id', show=False)
    item = Col('Item')
    price = Col('Price')
    quantity = Col('Quantity')
    store_name = Col('Store Name')
    address = Col('Address')
    date_to_purchase = Col('Date To Purchase')
    note = Col('Note')

    edit = LinkCol('Edit', 'edit', url_kwargs=dict(id='id'))
    delete = LinkCol('Delete', 'delete', url_kwargs=dict(id='id'))
