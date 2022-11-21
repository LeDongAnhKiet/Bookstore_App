from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100))
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        # c1 = Category(name='Văn học')
        # c2 = Category(name='Kinh tế')
        # c3 = Category(name='Kỹ năng')
        # c4 = Category(name='Sức khỏe')
        # c5 = Category(name='Truyện trẻ em')
        # c6 = Category(name='Lãng mạn')
        # c7 = Category(name='Khoa học')
        #
        # db.session.add_all([c1, c2, c3, c4, c5, c6, c7])
        # db.session.commit()

        p1 = Product(name='Thanh gươm do dự', price=199000,
                     image='https://nhasachphuongnam.com/images/thumbnails/900/900/detailed/237/thanh-guom-do-du.jpg'
                     , quantity=200, category_id=1)
        p2 = Product(name='Lũ Trẻ Đường Tàu', price=129000,
                     image='https://nhasachphuongnam.com/images/detailed/237/lu-tre-duong-tau.jpg'
                     , quantity=200, category_id=2)
        p3 = Product(name='Thanh gươm do dự', price=199000,
                     image='https://nhasachphuongnam.com/images/thumbnails/900/900/detailed/237/thanh-guom-do-du.jpg'
                     , quantity=200, category_id=3)
        db.session.add_all([p1, p2, p3])
        db.session.commit()