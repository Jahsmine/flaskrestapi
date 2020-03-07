from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
import secure
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)
CORS(app)  # открывает доступ к API ресурсу всем сайтам итд
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # TODO: ???????????????????
app.secret_key = 'jose'
api = Api(app)




jwt = JWT(app, secure.authenticate, secure.identity)  # /auth

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)