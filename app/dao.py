from app.models import Category, Book
from app import db


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

