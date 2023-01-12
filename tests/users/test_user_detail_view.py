from rest_framework.test import APITestCase
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from tests.factories import create_user_with_token

import ipdb

User: AbstractUser = get_user_model()


class UserDetailViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        user_2_data = {
            "email": "wigo_rossim@mail.com",
            "username": "wigo_rossim",
            "password": "1234",
            "total_balance": 8000,
            "goal_balance": 2000,
        }

        cls.user_2, token_2 = create_user_with_token(user_data=user_2_data)
        cls.access_token_2 = str(token_2.access_token)

        cls.BASE_URL = f"/api/users/{cls.user_1.id}/"

        cls.maxDiff = None

    def test_retrieve_user_without_token(self):
        response = self.client.get(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em GET rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_data = {"detail": "Authentication credentials were not provided."}
        returned_data = response.json()
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_data}. Resposta recebida: {returned_data}"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_retrieve_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.get(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_403_FORBIDDEN
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em GET rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        returned_message = response.json()
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_message}. Resposta recebida: {returned_message}"
        self.assertDictEqual(expected_message, returned_message, msg)

    def test_retrieve_user_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_200_OK
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em GET rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_fields = {
            "id",
            "username",
            "email",
            "is_active",
            "is_healthy",
            "total_balance",
            "goal_balance",
            "current_balance",
        }
        returned_data: dict = response.json()
        returned_fields = set(returned_data.keys())
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_fields}. Resposta recebida: {returned_fields}"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_soft_delete_user_without_token(self):
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em DELETE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_message = {"detail": "Authentication credentials were not provided."}
        returned_message = response.json()
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_message}. Resposta recebida: {returned_message}"
        self.assertDictEqual(expected_message, returned_message, msg)

    def test_soft_delete_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_403_FORBIDDEN
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em DELETE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        returned_message = response.json()
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_message}. Resposta recebida: {returned_message}"
        self.assertDictEqual(expected_message, returned_message, msg)

    def test_soft_delete_user_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_204_NO_CONTENT
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em DELETE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_update_user_without_token(self):
        response = self.client.patch(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em UPDATE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_message = {"detail": "Authentication credentials were not provided."}
        returned_message = response.json()
        msg = f"Erro em UPDATE rota {self.BASE_URL}. Resposta esperada: {expected_message}. Resposta recebida: {returned_message}"
        self.assertDictEqual(expected_message, returned_message, msg)

    def test_update_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.patch(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_403_FORBIDDEN
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em UPDATE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        returned_message = response.json()
        msg = f"Erro em UPDATE rota {self.BASE_URL}. Resposta esperada: {expected_message}. Resposta recebida: {returned_message}"
        self.assertDictEqual(expected_message, returned_message, msg)

    def test_update_user_success(self):
        info_to_patch = {
            "id": "está errado",
            "email": "lais_bomtempo_sm@mail.com",
            "current_balance": 2000,
            "total_balance": 7000,
            "goal_balance": 2000,
            "is_active": False,
            "is_healthy": False
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.patch(self.BASE_URL, data=info_to_patch, format="json")

        expected_status_code = status.HTTP_200_OK
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em UPDATE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_data = {
            "id": str(self.user_1.id),
            "email": info_to_patch["email"],
            "username": self.user_1.username,
            "total_balance": "5000.00",
            "current_balance": "0.00",
            "goal_balance": "2000.00",
            "is_active": self.user_1.is_active,
            "is_healthy": False,
        }
        returned_data = response.json()
        msg = f"Erro em UPDATE rota {self.BASE_URL}. Resposta esperada: {expected_data}. Resposta recebida: {returned_data}"
        self.assertDictEqual(expected_data, returned_data, msg)
