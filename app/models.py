from sqlalchemy import Text, Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import db, app
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime
import hashlib


class UserRole(UserEnum):
    Customer = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False, unique=True)
    Books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


class TypeofCreator(BaseModel):
    __tablename__ = 'TypeOfCreator'

    name = Column(String(50), nullable=False, unique=True)
    Creators = relationship('Creator', backref='typeofcreator', lazy=True)

    def __str__(self):
        return self.name


book_creator = db.Table('book_creator',
                        Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                        Column('creator_id', ForeignKey('creator.id'), nullable=False, primary_key=True))


class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    description = Column(Text)
    image = Column(String(130))
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    creators = relationship('Creator', secondary='book_creator', lazy='subquery', backref=backref('book', lazy=True))
    order_details = relationship('OrderDetails', backref='Book', lazy=True)

    def __str__(self):
        return self.name


class Creator(BaseModel):
    __tablename__ = 'creator'

    name = Column(String(50), nullable=False)
    type_id = Column(Integer, ForeignKey(TypeofCreator.id), nullable=False)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.Customer)
    order = relationship('Order', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Order(BaseModel):
    __tablename__ = 'order'

    date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
<<<<<<< HEAD
    OrderDetail = relationship('OrderDetails', backref='order', lazy=True)
=======
    OrderDetail_id = relationship('OrderDetails', backref='receipt', lazy=True)
>>>>>>> parent of a2d0e46 (xu ly cart)

    def __str__(self):
        return self.name


class OrderDetails(BaseModel):
    __tablename__ = 'orderdetails'

    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        c1 = Category(name='Sách giáo khoa')
        c2 = Category(name='Ngoại ngữ')
        c3 = Category(name='Khoa học')
        c4 = Category(name='Văn học - tiểu thuyết')

        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='Duong', username='admin', password=password, user_role=UserRole.ADMIN,
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729569/fi9v6vdljyfmiltegh7k.jpg')
        db.session.add(u)
        db.session.commit()

        d1 = TypeofCreator(name='Tác giả')
        d2 = TypeofCreator(name='Dịch giả')

        a1 = Creator(name='Robert Cecil Martin', type_id=1)
        b1 = Book(name='Clean Code', price=299000, image='https://cdn0.fahasa.com/media/catalog/product/3/9/393129.jpg',
                  quantity=200, category_id=3)

        a2 = Creator(name='Alice Schroeder', type_id=1)
        b2 = Book(name='Cuộc Đời Và Sự Nghiệp Của Warren Buffett', price=529000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/2/z2347757265330_74b3b3541a95b12454cbde947ccc635e.jpg',
                  quantity=300, category_id=4)

        a3 = Creator(name='Marry Buffet', type_id=1)
        a4 = Creator(name='Sean Seah', type_id=1)
        b3 = Book(name='7 Phương Pháp Đầu Tư Warren Buffet', price=143000,
                  image='https://cdn0.fahasa.com/media/catalog/product/8/9/8936066694131.jpg',
                  quantity=300, category_id=4)

        a5 = Creator(name='Mai Lan Hương', type_id=1)
        a6 = Creator(name='Hà Thanh Uyên', type_id=2)
        b4 = Book(name='Giải Thích Ngữ Pháp Tiếng Anh ', price=139000,
                  image='https://cdn0.fahasa.com/media/catalog/product/z/3/z3097453775918_7ea22457f168a4de92d0ba8178a2257b.jpg'
                  , quantity=300, category_id=2)

        a7 = Creator(name='Bộ Giáo Dục Và Đào Tạo', type_id=1)
        b5 = Book(name='Sách Giáo Khoa Bộ Lớp 12', price=180000,
                  image='https://cdn0.fahasa.com/media/catalog/product/3/3/3300000015422-1.jpg'
                  , quantity=300, category_id=1)

        db.session.add_all([d1, d2])
        db.session.commit()

        db.session.add_all([a1, a2, a3, a4, a5, a6, a7])
        db.session.commit()

        db.session.add_all([b1, b2, b3, b4, b5])
        db.session.commit()
