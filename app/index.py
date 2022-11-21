from flask import render_template, request, redirect
from app import app, dao


@app.route("/")
def index():
    products = dao.load_products(category_id=request.args.get('category_id'),
                                 kw=request.args.get('keyword'))
    return render_template('index.html', products=products)


@app.context_processor
def common_attribute():
    categories = dao.load_categories()
    return {
        'categories': categories
    }


if __name__ == '__main__':
    app.run(debug=True)
