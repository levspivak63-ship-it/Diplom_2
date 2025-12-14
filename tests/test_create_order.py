# test_create_order.py

import allure
import pytest
import requests
from data import TestData

class TestCreateOrder:
    """Тесты для создания заказа."""
    
    @allure.title("Создание заказа с валидными ингредиентами и авторизацией")
    
    def test_create_order_with_auth_success(self, auth_token, valid_ingredients):
        with allure.step("1. Подготовка данных заказа с валидными ингредиентами"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": valid_ingredients}
        with allure.step("2. Отправка POST запроса на создание заказа"):
            response = requests.post(f"{TestData.BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        with allure.step("3. Проверка ответа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "order" in response_data
    
    @allure.title("Создание заказа без авторизации")
    
    def test_create_order_without_auth_failure(self, valid_ingredients):
        with allure.step("1. Подготовка данных заказа"):
            order_data = {"ingredients": valid_ingredients}
        with allure.step("2. Отправка POST запроса без токена авторизации"):
            response = requests.post(f"{TestData.BASE_URL}/orders", json=order_data, timeout=10)
        with allure.step("3. Проверка что заказ создается без авторизации"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
    
    @allure.title("Создание заказа с ингредиентами")
    
    def test_create_order_with_ingredients_success(self, auth_token, valid_ingredients):
        with allure.step("1. Подготовка данных заказа"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": valid_ingredients}
        with allure.step("2. Отправка POST запроса с ингредиентами"):
            response = requests.post(f"{TestData.BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        with allure.step("3. Проверка что заказ создается"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
    
    @allure.title("Создание заказа без ингредиентов")
    
    def test_create_order_without_ingredients_failure(self, auth_token):
        with allure.step("1. Подготовка данных заказа без ингредиентов"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": []}
        with allure.step("2. Отправка POST запроса с пустым списком ингредиентов"):
            response = requests.post(f"{TestData.BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        with allure.step("3. Проверка ошибки создания заказа без ингредиентов"):
            assert response.status_code == 400
            response_data = response.json()
            assert response_data["message"] == "Ingredient ids must be provided"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    
    def test_create_order_with_invalid_ingredient_hash_failure(self, auth_token):
        with allure.step("1. Подготовка данных заказа с неверным хешем ингредиентов"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": [TestData.INVALID_INGREDIENT_HASH, "another_invalid_hash"]}
        with allure.step("2. Отправка POST запроса с неверным хешем ингредиентов"):
            response = requests.post(f"{TestData.BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        with allure.step("3. Проверка ошибки создания заказа с неверным хешем ингредиентов"):
            assert response.status_code == 500