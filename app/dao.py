from flask_login import current_user
from app.models import Category, Book, User, Order, OrderDetails, TypeofCreator
from app import db
from sqlalchemy import func
import hashlib


def load_categories():
    return Category.query.all()


def load_type():
    return TypeofCreator.query.all()


def load_books(category_id=None, kw=None):
    query = Book.query

    if category_id:
        query = query.filter(Book.category_id.__eq__(category_id))

    if kw:
        query = query.filter(Book.name.contains(kw))

    return query.all()


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def load_book_has_same_cate(book_id):
    b = Book.query.get(book_id)
    # return Book.query.join(Category, Book.category_id==Category.id)\
    #     .filter(Category.id.__eq__(b.category_id)).limit(2).all() .limit() = select top(2)
    return Book.query.join(Category, Book.category_id == Category.id) \
        .filter(Category.id.__eq__(b.category_id)).all()


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


def update_profile(user_id, name, address, phone):
    user = User.query.get(user_id)
    user.name = name
    user.address = address
    user.phone = phone
    db.session.commit()


def change_pw(user_id, old, new):
    user = User.query.get(user_id)
    oldpw = str(hashlib.md5(old.encode('utf-8')).hexdigest())
    if oldpw.__eq__(user.password):
        user.password = str(hashlib.md5(new.encode('utf-8')).hexdigest())
        db.session.commit()
        return True
    return False


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_order(cart):
    if cart:
        r = Order(user=current_user)
        db.session.add(r)
        for c in cart.values():
            d = OrderDetails(quantity=c['quantity'], price=c['price'], order=r, book_id=c['id'])
            db.session.add(d)
        try:
            db.session.commit()
        except:
            return False
        else:
            return True


def count_book_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Book.id)) \
        .join(Book, Book.category_id.__eq__(Category.id), isouter=True) \
        .group_by(Category.id).order_by(Category.name).all()



def stats_revenue_by_book(kw=None, from_date=None, to_date=None):
    query = db.session.query(Book.id, Book.name, func.sum(OrderDetails.quantity * OrderDetails.price)) \
                .join(OrderDetails, OrderDetails.book_id.__eq__(Book.id)) \
                .join(Order, OrderDetails.order_id.__eq__(Order.id))
    if kw:
        query = query.filter(Book.name.contains(kw))
    if from_date:
        query = query.filter(Order.created_date.__ge__(from_date))
    if to_date:
        query = query.filter(Order.created_date.__le__(to_date))
    return query.group_by(Book.id).all()


def load_order_history(user_id):
    u = User.query.get(user_id)
    return Order.query.join(User, User.id == Order.user_id).filter(Order.user_id == user_id).all()


def load_orderdetails(od_id):
    return Order.query.get(od_id)


if __name__ == '__main__':
    from app import app

    with app.app_context():
        print(count_book_by_cate())