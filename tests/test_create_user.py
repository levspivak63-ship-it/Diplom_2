import allure
import pytest
import requests
from data import BASE_URL
from helper import generate_user_data

class TestCreateUser:
    """Тесты для создания пользователя."""
    
    @allure.title("Создать уникального пользователя")
    
    def test_create_unique_user_success(self):
        """Создать уникального пользователя."""
        with allure.step("Подготовка уникальных данных"):
            user_data = generate_user_data()
        
        with allure.step("Отправка запроса на регистрацию"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
        
        with allure.step("Проверка успешной регистрации"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]
        
        with allure.step("Удаление пользователя"):
            headers = {"Authorization": response_data["accessToken"]}
            requests.delete(f"{BASE_URL}/auth/user", headers=headers, timeout=5)
    
    @allure.title("Создать пользователя, который уже зарегистрирован")
    
    def test_create_existing_user_failure(self):
        """Создать пользователя, который уже зарегистрирован."""
        with allure.step("Создание первого пользователя"):
            user_data = generate_user_data()
            response1 = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
            assert response1.status_code == 200
        
        with allure.step("Попытка повторной регистрации"):
            response2 = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
            assert response2.status_code == 403
            response_data = response2.json()
            assert response_data["success"] is False
        
        with allure.step("Удаление пользователя"):
            headers = {"Authorization": response1.json()["accessToken"]}
            requests.delete(f"{BASE_URL}/auth/user", headers=headers, timeout=5)
    
    @allure.title("Создать пользователя без заполнения одного из обязательных полей")
    
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_failure(self, missing_field):
        """Создать пользователя и не заполнить одно из обязательных полей."""
        with allure.step(f"Подготовка данных без поля {missing_field}"):
            user_data = generate_user_data()
            del user_data[missing_field]
        
        with allure.step("Попытка регистрации с неполными данными"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
            assert response.status_code in [400, 403]
            response_data = response.json()
            assert response_data["success"] is False