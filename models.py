from flask_login import UserMixin
from sqlalchemy.orm import column_property
from sqlalchemy import select, func
from . import db


#  Models are classes to work with SQL database
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    img_name = db.Column(db.String)


class Item_category(db.Model):
    __tablename__ = 'item_category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(500))
    item_count = column_property(select([func.count(Items.id)]).where(Items.category == id))


class Qty_changelog(db.Model):
    __tablename__ = 'qty_changelog'
    id = db.Column(db.Integer, primary_key=True)
    change_time = db.Column(db.DateTime, nullable=False)
    item_id = db.Column(db.String(100), nullable=False)
    qty_old = db.Column(db.Integer, nullable=False)
    qty_new = db.Column(db.Integer, nullable=False)
