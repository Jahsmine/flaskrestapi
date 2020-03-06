from werkzeug.security import safe_str_cmp  # так лучше всего сравнивать строки через этот модуль
from models.user_model import UserModel


# функция аутентификации

def authenticate(username, password):
    user = UserModel.find_by_the_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# функция присваинвания id - токена


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
