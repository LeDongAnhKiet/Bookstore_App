from app import db, app, dao
from app.models import Category, Book, UserRole
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


class BookView(ModelView):
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


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue_by_book(kw=request.args.get('kw'),
                                          from_date=request.args.get('from_date'),
                                          to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)


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
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))