from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_transaction


class TransactionDetailViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)

        user_2_data = {
            "email": "wigo_rossim@mail.com",
            "username": "wigoRossim",
            "password": "1234",
            "total_balance": 8000,
            "goal_balance": 2000,
        }
        cls.user_2, token_2 = create_user_with_token(user_data=user_2_data)
        cls.access_token_2 = str(token_2.access_token)

        cls.transaction_user_1 = create_transaction(cls.user_1)

        cls.BASE_URL = f"/api/transactions/{cls.transaction_user_1.id}/"

        cls.maxDiff = None

    def test_retrieve_transaction_without_token(self):
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

    def test_retrieve_transaction_with_another_user_token(self):
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

    def test_retrieve_transaction_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_200_OK
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em GET rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_data = {
            "id": self.transaction_user_1.id,
            "user": self.user_1.id,
            "type": "cash out",
            "date": self.transaction_user_1.date,
            "name": "aluguel",
            "value": 1500,
        }
        returned_data = response.json()
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_data}. Resposta recebida: {returned_data}"
        self.assertDictEqual(expected_data, returned_data, msg)

    def test_delete_transaction_without_token(self):
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_401_UNAUTHORIZED
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em GET rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_message = {"detail": "Authentication credentials were not provided."}
        returned_message = response.json()
        msg = f"Erro em GET rota {self.BASE_URL}. Resposta esperada: {expected_message}. Resposta recebida: {returned_message}"
        self.assertDictEqual(expected_message, returned_message, msg)

    def test_delete_transaction_with_another_user_token(self):
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

    def test_delete_transaction_success(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.BASE_URL, format="json")

        expected_status_code = status.HTTP_204_NO_CONTENT
        returned_status_code = response.status_code
        msg = (
            "STATUS CODE INCORRETO em DELETE rota "
            + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
        )
        self.assertEqual(expected_status_code, returned_status_code, msg)

    def test_update_transaction_without_token(self):
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

    def test_update_transaction_with_another_user_token(self):
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

    def test_update_transaction_success(self):
        info_to_patch = {
            "id": "está errado",
            "user": "está errado",
            "type": "cash in",
            "date": "está errado",
            "name": "extra venda brigadeiros",
            "value": 200,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)

        with self.subTest():
            expected_current_balance = (
                self.user_1.current_balance
                + self.transaction_user_1.value
                + info_to_patch.value
            )

            response = self.client.patch(
                self.BASE_URL, data=info_to_patch, format="json"
            )
            returned_current_balance = self.user_1.current_balance
            msg = f"Verifique se está atualizando o user current_balance corretamente. Esperado: current_balance={expected_current_balance}. Recebido: current_balance={returned_current_balance}"
            self.assertEqual(expected_current_balance, returned_current_balance, msg)

        with self.subTest():
            expected_status_code = status.HTTP_200_OK
            returned_status_code = response.status_code
            msg = (
                "STATUS CODE INCORRETO em UPDATE rota "
                + f"`{self.BASE_URL}`. Esperado: {expected_status_code}; Recebido: {returned_status_code}"
            )
            self.assertEqual(expected_status_code, returned_status_code, msg)

        expected_data = {
            "id": self.transaction_user_1.id,
            "user": self.user_1.id,
            "type": info_to_patch["type"],
            "date": self.transaction_user_1.date,
            "name": info_to_patch["name"],
            "value": info_to_patch["value"],
        }
        returned_data = response.json()
        msg = f"Erro em UPDATE rota {self.BASE_URL}. Resposta esperada: {expected_data}. Resposta recebida: {returned_data}"
        self.assertDictEqual(expected_data, returned_data, msg)
