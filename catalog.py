from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from .models import Item_category, Items, Qty_changelog
from . import db, Config
import datetime, random, os


catalog = Blueprint('catalog', __name__)


@catalog.route('/goods')
@login_required
def goods():
    line = Item_category.query.all()

    return render_template('goods.html', line=line)


@catalog.route('/item', methods=['GET'])
@login_required
def items():
    id = request.values.get('id')
    page = request.values.get('page')
    if page == None:
        page = 1
    else:
        page = int(page)
    line = Items.query.filter_by(category=id).order_by(Items.title).paginate(page=page, per_page=5)
    return render_template('item.html', line=line, id=id)


@catalog.route('/cat_edit', methods=['POST', 'GET'])
@login_required
def cat_edit():
    id = request.values.get('id')
    cat = Item_category.query.filter_by(id=id).first()
    title = request.form.get('title')
    if title is not None:
        desc = request.form.get('description')
        cat.title = title
        cat.description = desc
        db.session.commit()
        return redirect(url_for('catalog.goods'))
    else:
        res = [cat.title, cat.description]
        return render_template('cat_edit.html', line=res, id=id)


@catalog.route('/cat_add', methods=['POST', 'GET'])
@login_required
def cat_add():
    title = request.form.get('title')
    if title is not None:
        desc = request.form.get('description')
        new_cat = Item_category(title=title, description=desc)
        db.session.add(new_cat)
        db.session.commit()
        return redirect(url_for('catalog.goods'))
    else:
        return render_template('cat_add.html')


@catalog.route('/cat_delete', methods=['GET'])
@login_required
def cat_del():
    id = request.values.get('id')
    cat = Item_category.query.filter_by(id=id).first()
    yes = request.values.get('yes')
    if yes is not None:
        db.session.delete(cat)
        db.session.commit()
        return redirect(url_for('catalog.goods'))
    else:
        confirm = url_for('catalog.cat_del', id=id, yes=1)
        cancel = url_for('catalog.goods')
        return render_template('confirm.html', title=cat.title, confirm=confirm, cancel=cancel)


@catalog.route('/item_edit', methods=['POST', 'GET'])
@login_required
def item_edit():
    id = request.values.get('id')
    item = Items.query.filter_by(id=id).first()
    title = request.form.get('title')
    if title is not None:
        desc = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        category = request.form.get('category')
        img = request.files.get('new_img')
        image = save_pic(img)
        if item.quantity != int(quantity):
            new_change = Qty_changelog(change_time=datetime.datetime.utcnow(), item_id=item.id, qty_old=item.quantity,
                                   qty_new=quantity)
            db.session.add(new_change)
        item.title = title
        item.description = desc
        item.price = price
        item.quantity = quantity
        item.category = category
        if image is not None:
            try:
                os.remove(Config.ROOT_PATH + Config.PICPATH + item.img_name)
            except:
                pass
            item.img_name = image
        db.session.commit()
        return redirect(url_for('catalog.items', id=category))
    else:
        all_cat = Item_category.query.with_entities(Item_category.id, Item_category.title).all()
        return render_template('item_edit.html', item=item, cats=all_cat, path=Config.PICPATH)


@catalog.route('/item_add', methods=['POST', 'GET'])
@login_required
def item_add():
    title = request.form.get('title')
    if title is not None:
        desc = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        category = request.form.get('category')
        img = request.files.get('new_img')
        image = save_pic(img)
        new_item = Items(title=title, description=desc, price=price, quantity=quantity, category=category, img_name=image)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('catalog.items', id=category))
    else:
        all_cat = Item_category.query.with_entities(Item_category.id, Item_category.title).all()
        return render_template('item_add.html', id=id, cats=all_cat)


@catalog.route('/item_delete', methods=['GET'])
@login_required
def item_del():
    id = request.values.get('id')
    item = Items.query.filter_by(id=id).first()
    yes = request.values.get('yes')
    if yes is not None:
        try:
            os.remove(Config.ROOT_PATH + Config.PICPATH + item.img_name)
        except:
            pass
        Qty_changelog.query.filter_by(item_id=item.id).delete()
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('catalog.items', id=item.category))
    else:
        confirm = url_for('catalog.item_del', id=id, yes=1)
        cancel = url_for('catalog.items', id=item.category)
        return render_template('confirm.html', title=item.title, confirm=confirm, cancel=cancel)


@catalog.route('/info', methods=['GET'])
def info():
    id = request.values.get('id')
    item = Items.query.filter_by(id=id).first()
    change = Qty_changelog.query.filter_by(item_id=id).order_by(Qty_changelog.change_time).all()
    null_list = []
    return render_template('info.html', item=item, change=change, null=null_list, path=Config.PICPATH)


def save_pic(img):
    try:
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF']
        if img is not None and '.' in img.filename and img.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
            nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            randomNum = random.randint(0, 100)
            if randomNum <= 10:
                randomNum = str(0) + str(randomNum)
            uniqueNum = str(nowTime) + str(randomNum)
            picurl = Config.ROOT_PATH + Config.PICPATH + uniqueNum + img.filename
            img.save(picurl)
            return uniqueNum + img.filename
        else:
            return None
    except Exception as e:
        return str(e)