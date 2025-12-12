import allure
import pytest
import requests
import json
from data import BASE_URL, EXISTING_USER

class TestLoginUser:
    """Тесты для авторизации пользователя."""
    
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user_success(self):
        """Вход под существующим пользователем."""
        with allure.step("Подготовка данных для входа"):
            login_data = {
                "email": EXISTING_USER["email"],
                "password": EXISTING_USER["password"]
            }
        
        with allure.step("Отправка запроса на вход"):
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=10)
        
        with allure.step("Проверка успешного входа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert "user" in response_data
            assert response_data["user"]["email"] == EXISTING_USER["email"]
    
    @allure.title("Вход с неверным логином и паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_wrong_credentials_failure(self):
        """Вход с неверным логином и паролем."""
        with allure.step("Подготовка неверных данных"):
            wrong_credentials = {
                "email": "wrong_email@example.com",
                "password": "wrong_password"
            }
        
        with allure.step("Попытка входа с неверными данными"):
            response = requests.post(f"{BASE_URL}/auth/login", json=wrong_credentials, timeout=10)
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert "message" in response_data