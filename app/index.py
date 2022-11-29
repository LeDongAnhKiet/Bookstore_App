from flask import render_template, request, redirect
from app import app, dao, admin, login
from flask_login import login_user, logout_user, login_required
from app.decorator import annonynous_user
import cloudinary.uploader


@app.route("/")
def index():
    products = dao.load_products(category_id=request.args.get('category_id'),
                                 kw=request.args.get('keyword'))
    return render_template('index.html', products=products)


@app.route('/products/<int:product_id>')
def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/login', methods=['get', 'post'])
@annonynous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect('/')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        username = request.form['username']
        if not " " in username and not " " in password:
            if password.__eq__(confirm):
                try:
                    m = dao.register(name=request.form['name'],
                                     password=password,
                                     username=username)
                    if m:
                        err_msg = 'Đăng ký thành công!!!'
                        return render_template('login.html', err_msg=err_msg)
                    else:
                        err_msg = 'Username đã tồn tại!'
                except:
                    err_msg = 'Đã có lỗi xảy ra!'
            else:
                err_msg = 'Mật khẩu không khớp!'
        else:
            err_msg = 'Username và Password không được chứa khoảng trắng!'

    return render_template('register.html', err_msg=err_msg)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attribute():
    categories = dao.load_categories()
    return {
        'categories': categories
    }


if __name__ == '__main__':
    app.run(debug=True)
