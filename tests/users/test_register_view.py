from rest_framework.test import APITestCase
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


User: AbstractUser = get_user_model()


class UserRegistrationViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

        cls.maxDiff = None

    def test_user_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        resulted_data: dict = response.json()
        expected_fields = {
            "email",
            "password",
            "total_balance",
            "name",
        }
        returned_fields = set(resulted_data.keys())
        msg = (
            "Faltam chaves obrigatórias na requisição"
            + f"Esperado: {expected_fields}. Recebido: {returned_fields}"
        )
        self.assertSetEqual(expected_fields, returned_fields, msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em POST rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_user_creation_success(self):
        register_data = {
            "email": "lais_bomtempo@mail.com",
            "name": "Laís Bomtempo",
            "password": "1234",
            "total_balance": 5000,
            "goal_balance": 1000,
        }

        response = self.client.post(self.BASE_URL, data=register_data, format="json")

        added_user = User.objects.last()

        expected_data = {
            "id": added_user.pk,
            "email": "lais_bomtempo@mail.com",
            "name": "Laís Bomtempo",
            "total_balance": 5000,
            "goal_balance": 1000,
            "current_balance": 5000,
            "is_active": True,
            "is_healthy": True,
        }
        returned_data = response.json()
        msg = f"Erro em POST rota {self.BASE_URL}. Resposta esperada: {expected_data}. Resposta recebida: {returned_data}"
        self.assertDictEqual(expected_data, returned_data, msg)

        msg = "Verifique se o password foi hasheado corretamente"
        self.assertTrue(added_user.check_password(register_data["password"]), msg)

        expected_status_code = status.HTTP_201_CREATED
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em POST rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_non_unique_email_user_creation(self):
        register_data = {
            "email": "lais_bomtempo@mail.com",
            "name": "Laís Bomtempo",
            "password": "1234",
            "total_balance": 5000,
            "goal_balance": 1000,
        }

        User.objects.create_user(**register_data)
        response = self.client.post(self.BASE_URL, data=register_data, format="json")

        returned_data = response.json()
        expected_fields = {"email"}
        returned_fields = set(returned_data.keys())
        msg = f"Erro em POST rota {self.BASE_URL}. Fields esperados: {expected_fields}. Fields recebidos: {returned_fields}"
        self.assertSetEqual(expected_fields, returned_fields, msg)

        returned_email_message = returned_data["email"][0]
        expected_email_message = "This field must be unique"

        msg = f"Esperado mensagem de erro: {expected_email_message}. Recebido: {returned_email_message}"
        self.assertEqual(expected_email_message, returned_email_message, msg)

        expected_status_code = status.HTTP_400_BAD_REQUEST
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em POST rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)
