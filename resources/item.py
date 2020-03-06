from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel


class Item(Resource):
    # парсер класса для извлечения информации из запроса
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This cannot be left blank!"
                        )

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="Every item needs Store ID!"
                        )

    # модификатор аутентификации
    @jwt_required()
    def get(self, name):
        # получаем данные обьекта из БД если он существует - возвращаем его
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        # ищем в совпадения в БД
        if ItemModel.find_by_name(name):
            return {"message": "An item with {0} already exists.".format(name)}, 400  # status code 400 "Bad request"
        # получаем словарь данных для записи и записываем в переменную
        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"], data["store_id"])
        # подключаемся к БД и записывем данные
        try:
            item.save_to_db()
        except Exception as err:
            return {"message": "An exception {0} raised".format(err)}, 500
            # возвращаем обьект данных и код статуса
        return item.json(), 201  # 201 status code "201 CREATED"

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item {0} deleted".format(name)}
        return {"message": "Item {0} not found".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": list(map(lambda x: x.json(), ItemModel.query.all()))}

