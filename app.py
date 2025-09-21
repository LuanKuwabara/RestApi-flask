from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re

app = Flask(__name__)

app.config["MONGODB_SETTINGS"] = [
    {
        "db": "users",
        "host": "mongo",
        "port": 27017,
        "username": "admin",
        "password": "admin",
        "alias": "default",
    }
]

api = Api(app)
db = MongoEngine(app)

parser = reqparse.RequestParser()
parser.add_argument('first_name',
                    type=str,
                    required=True,
                    help="This field cannot be blank")
parser.add_argument('last_name',
                    type=str,
                    required=True,
                    help="This field cannot be blank")
parser.add_argument('cpf',
                    type=str,
                    required=True,
                    help="This field cannot be blank")
parser.add_argument('email',
                    type=str,
                    required=True,
                    help="This field cannot be blank")
parser.add_argument('birth_date',
                    type=str,
                    required=True,
                    help="This field cannot be blank")


class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.EmailField(required=True)
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    birth_date = db.DateTimeField(required=True)


def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if int(cpf[i]) != digito:
            return False
    return True

class Users(Resource):
    def get(self):
        return {'message': 'user 1'}


class User(Resource):
    def post(self):
        data = parser.parse_args()
        if not validar_cpf(data['cpf']):
            return {'message': 'CPF Inválido'}, 400
        
        try:
            response = UserModel(**data).save()
            return {'message': f"Usuário {response} criado com sucesso!"}, 201
        except NotUniqueError:
            return {"message": "CPF já existente!"}, 400


    def get(self, cpf):
        return {'message': f'User with CPF {cpf}'}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
