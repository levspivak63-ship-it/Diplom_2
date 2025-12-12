import allure
import pytest
import requests
from data import BASE_URL

class TestCreateOrder:
    """Тесты для создания заказа."""
    
    @allure.title("Создание заказа с авторизацией")
    
    def test_create_order_with_auth_success(self, auth_token, valid_ingredients):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": valid_ingredients}
        
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
        assert "order" in response_data
    
    @allure.title("Создание заказа без авторизации")
    
    def test_create_order_without_auth_failure(self, valid_ingredients):
        order_data = {"ingredients": valid_ingredients}
        
        response = requests.post(f"{BASE_URL}/orders", json=order_data, timeout=10)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
    
    @allure.title("Создание заказа с ингредиентами")
    
    def test_create_order_with_ingredients_success(self, auth_token, valid_ingredients):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": valid_ingredients}
        
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True
    
    @allure.title("Создание заказа без ингредиентов")
    
    def test_create_order_without_ingredients_failure(self, auth_token):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": []}
        
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        
        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] is False
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    
    def test_create_order_with_invalid_ingredient_hash_failure(self, auth_token, invalid_ingredient_hash):
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": [invalid_ingredient_hash, "another_invalid_hash"]}
        
        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers, timeout=10)
        
        assert response.status_code == 500