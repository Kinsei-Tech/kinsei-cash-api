from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token


class CreateTransactionViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/transactions/"

        cls.maxDiff = None

        cls.user, token = create_user_with_token()
        cls.access_token = str(token.access_token)

    def test_transaction_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        returned_data: dict = response.json()
        expected_fields = {
            "type",
            "name",
            "value",
            "category",
        }
        returned_fields = set(returned_data.keys())
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

    def test_transaction_creation_without_token(self):

        with self.subTest():
            response = self.client.post(self.BASE_URL, data={}, format="json")
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            returned_status_code = response.status_code
            msg = (
                "STATUS CODE INCORRETO em POST rota "
                + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_data = {"detail": "Authentication credentials were not provided."}
        returned_data = response.json()
        msg = f"Erro em POST rota {self.BASE_URL}. Resposta esperada: {expected_data}. Resposta recebida: {returned_data}"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_transaction_creation_success(self):
        transaction_data = {
            "type": "cash out",
            "name": "aluguel",
            "category": "house_bills",
            "value": 1500,
        }

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.access_token))
        response = self.client.post(self.BASE_URL, data=transaction_data, format="json")

        with self.subTest():
            expected_current_balance = self.user.total_balance - transaction_data.value
            returned_current_balance = self.user.current_balance
            msg = f"Verifique se está atualizando o user current_balance corretamente. Esperado: current_balance={expected_current_balance}. Recebido: current_balance={returned_current_balance}"
            self.assertEqual(expected_current_balance, returned_current_balance, msg)

        with self.subTest():
            expected_status_code = status.HTTP_201_CREATED
            returned_status_code = response.status_code
            msg = (
                "STATUS CODE INCORRETO em POST rota "
                + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        returned_data = response.json()
        expected_fields = {"id", "user", "type", "date", "name", "value"}
        returned_fields = set(returned_data.keys())
        msg = f"Erro em POST rota {self.BASE_URL}. Fields esperados: {expected_fields}. Fields recebidos: {returned_fields}"
        self.assertSetEqual(expected_fields, returned_fields, msg)
