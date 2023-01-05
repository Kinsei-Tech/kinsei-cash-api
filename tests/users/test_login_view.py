from rest_framework.test import APITestCase
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


User: AbstractUser = get_user_model()


class UserLoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/login"

        cls.maxDiff = None

    def test_user_login_without_required_fields(self):
        response = self.client.post(
            self.BASE_URL,
            data={},
            format="json",
        )

        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            returned_status_code = response.status_code
            msg = (
                "STATUS CODE INCORRETO em POST rota "
                + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_fields = {
            "email",
            "password",
        }
        returned_fields = set(returned_data.keys())
        msg = "Verifique se a requisição apresenta as chaves obrigatórias: email e password."
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_login_success(self):
        register_data = {
            "email": "lais_bomtempo@mail.com",
            "name": "Laís Bomtempo",
            "password": "1234",
            "total_balance": 5000,
            "goal_balance": 1000,
        }
        User.objects.create_user(**register_data)
        login_data = {
            "email": "lais_bomtempo@email.com",
            "password": "1234",
        }

        with self.subTest():
            response = self.client.post(self.BASE_URL, data=login_data, format="json")
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "STATUS CODE INCORRETO em POST rota "
                + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_keys = {"access", "refresh"}
        returned_keys = set(response.json().keys())
        msg = (
            "Verifique se o token está sendo retornado corretamente "
            + f"em `{self.BASE_URL}`"
            + "Ele deve conter as keys access e refresh"
        )
        self.assertSetEqual(expected_keys, returned_keys, msg)

    def test_login_with_wrong_credentials(self):
        login_data = {
            "email": "email_nao_existente@email.com",
            "password": "111111",
        }

        with self.subTest():
            response = self.client.post(
                self.BASE_URL,
                data=login_data,
                format="json",
            )
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "STATUS CODE INCORRETO em POST rota "
                + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data: dict = response.json()
        expected_data = {"detail": "No active account found with the given credentials"}
        msg = (
            "Verifique se a mensagem de erro para credenciais inválidas está correta. "
            + f"Esperado: {expected_data}"
        )
        self.assertDictEqual(expected_data, returned_data, msg)
