from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel
import re
import traceback

# Define os argumentos esperados na requisição
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


# Validação de CPF
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


# Endpoint /users
class Users(Resource):
    def get(self):
        try:
            return jsonify(UserModel.objects())
        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}, 500


# Endpoint /user e /user/<cpf>
class User(Resource):
    def post(self):
        try:
            data = parser.parse_args()

            if not validar_cpf(data['cpf']):
                return {'message': 'CPF Inválido'}, 400

            response = UserModel(**data).save()
            return {'message': f"Usuário {response} criado com sucesso!"}, 201

        except NotUniqueError:
            return {"message": "CPF já existente!"}, 400

        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}, 500

    def get(self, cpf):
        try:
            response = UserModel.objects(cpf=cpf)
            if response:
                return jsonify(response)
            return {"message": "Usuário não existe no banco de dados!"}, 400

        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}, 500
