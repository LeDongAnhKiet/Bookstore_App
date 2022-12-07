from flask import render_template, request, redirect, session, jsonify
from app import app, dao, admin, login, utils
from flask_login import login_user, logout_user, login_required, current_user
from app.decorator import annonynous_user
import cloudinary.uploader


@app.route("/")
def index():
    page = request.args.get('page', 1, type=int)
    books = dao.load_books(category_id=request.args.get('category_id'),
                           kw=request.args.get('keyword'), page=page)

    return render_template('index.html', books=books)


@app.route('/books/<int:book_id>')
def details(book_id):
    p = dao.get_book_by_id(book_id)
    if not p:
        return redirect('/')
    else:
        books = dao.load_book_has_same_cate(book_id)
        tacgia = []
        minhhoa = []
        for i in p.creators:
            if i.type_id == 1:
                tacgia.append(i.name)
            if i.type_id == 2:
                minhhoa.append(i.name)
        return render_template('details.html', book=p, tacgia=tacgia, minhhoa=minhhoa, books=books)


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
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)

            n = request.args.get('next')
            return redirect(n if n else '/')

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
                    m = dao.register(name=request.form['name'], password=password,
                                     username=username)
                    if m:
                        # err_msg = 'Đăng ký thành công!!!'
                        return redirect('/login')
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


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    data = request.json

    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    id = str(data['id'])
    name = data['name']
    price = data['price']

    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/cart/<book_id>', methods=['put'])
def update_cart(book_id):
    key = app.config['CART_KEY']

    cart = session.get(key)
    if cart and book_id in cart:
        cart[book_id]['quantity'] = int(request.json['quantity'])

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/api/cart/<book_id>', methods=['delete'])
def delete_cart(book_id):
    key = app.config['CART_KEY']

    cart = session.get(key)
    if cart and book_id in cart:
        del cart[book_id]

    session[key] = cart

    return jsonify(utils.cart_stats(cart))


@app.route('/pay')
@login_required
def pay():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if dao.makepayment(cart=cart):
        del session[key]
    else:
        return jsonify({'status': 500})

    return jsonify({'status': 200})


@app.route('/preorder')
@login_required
def preorder():
    key = app.config['CART_KEY']
    cart = session.get(key)

    if dao.add_order(cart=cart):
        del session[key]
    else:
        return jsonify({'status': 500})

    return jsonify({'status': 200})


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@app.route('/edit', methods=['get', 'post'])
@login_required
def edit():
    err_msg = ''
    id = current_user.id
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        try:
            dao.update_profile(id, name, address, phone)
            return redirect('/account')
        except:
            err_msg = 'Đã có lỗi xảy ra!'

    return render_template('edit.html', err_msg=err_msg)


@app.route('/change-password', methods=['get', 'post'])
@login_required
def change_password():
    err_msg = ''
    id = current_user.id
    if request.method.__eq__('POST'):
        old_pw = request.form['oldpassword']
        new_pw = request.form['newpassword']
        confirm = request.form['confirm']
        if new_pw.__eq__(confirm):
            try:
                m = dao.change_pw(id, old_pw, new_pw)
                if m:
                    return redirect('/account')
                else:
                    err_msg = 'Mật khẩu cũ sai'
                    return render_template('change-password.html', err_msg=err_msg)
            except:
                err_msg = 'Đã có lỗi xảy ra!'
        else:
            err_msg = 'Nhập mật khẩu không khớp'

    return render_template('change-password.html', err_msg=err_msg)


@app.route('/order-history')
@login_required
def load_order():
    orders = dao.load_order_history(current_user.id)
    return render_template('order-history.html', orders=orders)


@app.route('/order-history/<int:order_id>')
@login_required
def order_details(order_id):
    p = dao.load_order_details(order_id)
    return render_template('orders.html', p=p)


@app.context_processor
def common_attribute():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


if __name__ == '__main__':
    app.run(debug=True)
