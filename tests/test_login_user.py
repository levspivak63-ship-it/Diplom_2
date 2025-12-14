# test_login_user.py

import allure
import pytest
import requests
from data import TestData

class TestLoginUser:
    """Тесты для авторизации пользователя."""
    
    @allure.title("Вход под существующим пользователем")
   
    def test_login_existing_user_success(self):
        """Вход под существующим пользователем."""
        with allure.step("Подготовка данных для входа"):
            login_data = {
                "email": TestData.EXISTING_USER["email"],
                "password": TestData.EXISTING_USER["password"]
            }
        
        with allure.step("Отправка запроса на вход"):
            response = requests.post(f"{TestData.BASE_URL}/auth/login", json=login_data, timeout=10)
        
        with allure.step("Проверка успешного входа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert "user" in response_data
            assert response_data["user"]["email"] == TestData.EXISTING_USER["email"]
    
    @allure.title("Вход с неверным логином и паролем")
    
    def test_login_wrong_credentials_failure(self):
        """Вход с неверным логином и паролем."""
        with allure.step("Подготовка неверных данных"):
            wrong_credentials = {
                "email": "wrong_email@example.com",
                "password": "wrong_password"
            }
        
        with allure.step("Попытка входа с неверными данными"):
            response = requests.post(f"{TestData.BASE_URL}/auth/login", json=wrong_credentials, timeout=10)
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["message"] == "email or password are incorrect"
            