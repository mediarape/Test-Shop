from flask import Blueprint, render_template, request
from .models import Items


items = Blueprint('items', __name__)


@items.route('/all-items', methods=['GET'])
def allitems():
    id = request.values.get('id')
    page = request.values.get('page')
    if page == None:
        page = 1
    else:
        page = int(page)
    line = Items.query.order_by(Items.title).paginate(page=page, per_page=10)
    return render_template('all-items.html', line=line, id=id)
