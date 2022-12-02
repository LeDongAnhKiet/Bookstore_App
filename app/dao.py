from flask_login import current_user

from app.models import Category, Book, User, TypeofCreator, Order, OrderDetails
from app import db
import hashlib


def load_categories():
    return Category.query.all()

def load_typeofcreator(type_id):
    return TypeofCreator.query.get(type_id)

def load_products(category_id=None, kw=None):
    query = Book.query

    if category_id:
        query = query.filter(Book.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Book.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Book.query.get(product_id)


def get_typeofcreator(product_id):
    p = get_product_by_id(product_id)
    type_list = []
    for i in p.creators:
        type_list.append(i.typeofcreator.id)

    type_list = set(type_list)
    return type_list


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register(name, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    if not bool(User.query.filter_by(username=username).first()):
        u = User(name=name, username=username.strip(), password=password)
        db.session.add(u)
        db.session.commit()
        return True
    else:
        return False

def add_receipt(cart):
    if cart:
        r = Order(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = OrderDetails(quantity=c['quantity'], price=c['price'], book_id=c['id'],
                               order=r)
            db.session.add(d)

        try:
            db.session.commit()
        except:
            return False
        else:
            return True


def get_user_by_id(user_id):
    return User.query.get(user_id)