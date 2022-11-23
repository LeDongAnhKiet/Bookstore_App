from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'Category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Contributor(BaseModel):
    __tablename__ = 'Contributor'
    name = Column(String(50), nullable=False)
    ContributorOfBook = relationship('ContributorOfBook', backref='contributor', lazy=True)

    def __str__(self):
        return self.name


class ContributorOfBook(BaseModel):
    __tablename__ = 'ContributorOfBook'
    contributor_id = Column(Integer, ForeignKey(Contributor.id), nullable=False)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False)
    infocontributor_id = Column(Integer, ForeignKey(InfoContributor.id), nullable=False)

    def __str__(self):
        return self.name


class Book(BaseModel):
    __tablename__ = 'Book'

    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100))
    quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    Contributorofbook_id = Column(Integer, ForeignKey(ContributorOfBook.id), nullable=False)

    def __str__(self):
        return self.name


class InfoContributor(BaseModel):
    __tablename__ = 'InfoContributor'
    name = Column(String(50), nullable=False)
    contributor_id = Column(Integer, ForeignKey(Contributor.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # c1 = Category(name='Sách giáo khoa')
        # c2 = Category(name='Ngoại ngữ')
        # c3 = Category(name='Kiến thức - Khoa học')
        # c4 = Category(name='Sách thiếu nhi')
        # c5 = Category(name='Tâm lý - Kỹ năng sống')
        # c6 = Category(name='Kinh tế')
        # c7 = Category(name='Văn học - tiểu thuyết')
        #
        # db.session.add_all([c1, c2, c3, c4, c5, c6, c7])
        # db.session.commit()

        # p1 = Book(name='Thanh gươm do dự', price=199000,
        #              image='https://nhasachphuongnam.com/images/thumbnails/900/900/detailed/237/thanh-guom-do-du.jpg'
        #              , quantity=200, category_id=1)
        # p2 = Book(name='Lũ Trẻ Đường Tàu', price=129000,
        #              image='https://nhasachphuongnam.com/images/detailed/237/lu-tre-duong-tau.jpg'
        #              , quantity=200, category_id=2)
        # p3 = Book(name='Thanh gươm do dự', price=199000,
        #              image='https://nhasachphuongnam.com/images/thumbnails/900/900/detailed/237/thanh-guom-do-du.jpg'
        #              , quantity=200, category_id=3)
        # db.session.add_all([p1, p2, p3])
        # db.session.commit()
