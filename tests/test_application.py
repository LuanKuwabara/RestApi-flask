import pytest
from application import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app("config.MockConfig")
        yield app.test_client()

    @pytest.fixture
    def valid_user(self):
        return {
            "first_name": "Luan",
            "last_name": "Kuwabara",
            "cpf": "911.559.460-22",
            "email": "lnkwbr@gmail.com",
            "birth_date": "2001-06-27"
        }

    @pytest.fixture
    def invalid_user(self):
        return {
            "first_name": "Luan",
            "last_name": "Kuwabara",
            "cpf": "911.559.460-20",
            "email": "lnkwbr@gmail.com",
            "birth_date": "2001-06-27"
        }

    def test_get_users(self, client):
        response = client.get("/users")
        assert response.status_code == 200

    def test_post_user(self, client, valid_user, invalid_user):
        response = client.post("/user", json=valid_user)
        assert response.status_code == 201
        assert b"sucesso" in response.data

        response = client.post("/user", json=invalid_user)
        assert response.status_code == 400
        data = response.get_json()
        assert "Inválido" in data["message"]

    def test_get_user(self, client, valid_user, invalid_user):
        response = client.get("/user/%s" % valid_user["cpf"])
        assert response.status_code == 200
        assert response.json[0]["first_name"] == "Luan"
        assert response.json[0]["last_name"] == "Kuwabara"
        assert response.json[0]["cpf"] == "911.559.460-22"
        assert response.json[0]["email"] == "lnkwbr@gmail.com"
        birth_date = response.json[0]["birth_date"]["$date"]
        assert birth_date == "2001-06-27T00:00:00Z"

        response = client.get("/user/%s" % invalid_user["cpf"])
        assert response.status_code == 400
        data = response.get_json()
        assert "Usuário não existe no banco de dados!" in data["message"]
