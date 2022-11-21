from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
import cloudinary


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost:3306/bookstoreDb?charset=utf8mb4' % quote('duong1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

cloudinary.config(cloud_name='dmfr3gngl', api_key='119749293867732', api_secret='R42-4n6WSoV-ChzSKYws7Nqy0g4')