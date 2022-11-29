from app.models import Category, Book, User
from app import db
import hashlib


def load_categories():
    return Category.query.all()


def load_products(category_id=None, kw=None):
    query = Book.query

    if category_id:
        query = query.filter(Book.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Book.name.contains(kw))

    return query.all()


def get_product_by_id(product_id):
    return Book.query.get(product_id)


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


def get_user_by_id(user_id):
    return User.query.get(user_id)