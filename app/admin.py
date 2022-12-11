from wtforms.validators import InputRequired, NumberRange

from app import db, app, dao, Rules
from app.models import Category, Book, UserRole, RestockDetails, GoodsRestock, Order
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class AuthenticatedModeView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class BookView(AuthenticatedModeView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    column_exclude_list = ['image']
    can_export = True
    column_export_list = ['id', 'name', 'description']
    column_labels = {
        'name': 'Tên sách',
        'description': 'Mô tả',
        'price': 'Giá'
    }
    page_size = 5
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }


class RestockDetailsView(AuthenticatedModeView):
    column_list = ()
    # validator wtforms
    form_args = {
        "quantity": {"validators": [InputRequired(), NumberRange(min=Rules.get('RestockNumber'))]},
        "Book": {"query_factory": lambda: Book.query.filter(Book.quantity < Rules.get('InStockNumber'))}
    }


class GoodsRestockView(AuthenticatedModeView):
    can_view_details = True
    column_hide_backrefs = False
    column_display_pk = True



class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats1 = dao.stats_revenue_by_cate(kw=request.args.get('kw'),
                                           month=request.args.get('month'))
        stats2 = dao.stats_frequency_by_book(kw=request.args.get('kw'),
                                             month=request.args.get('month'))
        return self.render('admin/stats.html', stats1=stats1, stats2=stats2)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class AdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_book_by_cate()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='Quản lý nhà sách', template_mode='bootstrap4', index_view=AdminView())
admin.add_view(AuthenticatedModeView(Category, db.session, name='Danh mục'))
admin.add_view(BookView(Book, db.session, name='Sách'))
admin.add_view(RestockDetailsView(RestockDetails, db.session, name='Sách nhập'))
admin.add_view(GoodsRestockView(GoodsRestock, db.session, name='phiếu nhập'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))
