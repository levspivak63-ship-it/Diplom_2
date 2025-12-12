"""Фикстуры для тестов."""

import pytest
import requests
from data import BASE_URL
from helper import generate_user_data

@pytest.fixture
def create_user():
    """
    Фикстура для создания пользователя.
    Возвращает данные созданного пользователя.
    Удаляет пользователя после теста.
    """
    # 1. Генерируем уникальные данные
    user_data = generate_user_data()
    
    # 2. Регистрируем пользователя
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
    
    # 3. Получаем токен (если регистрация успешна)
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get("accessToken")
        user_data["access_token"] = access_token
        user_data["response_data"] = response_data
    else:
        # Если регистрация не удалась, все равно возвращаем данные
        user_data["access_token"] = None
        user_data["response_data"] = response.json()
    
    # 4. Возвращаем данные пользователя
    yield user_data
    
    # 5. Удаляем пользователя после теста (если был создан)
    if user_data.get("access_token"):
        try:
            headers = {"Authorization": user_data["access_token"]}
            requests.delete(f"{BASE_URL}/auth/user", headers=headers, timeout=5)
        except Exception:
            pass

@pytest.fixture
def auth_token(create_user):
    """Фикстура для получения токена авторизации."""
    token = create_user.get("access_token")
    if not token:
        pytest.skip("Не удалось получить токен авторизации")
    return token

@pytest.fixture
def valid_ingredients():
    """Фикстура для получения валидных ингредиентов из API."""
    response = requests.get(f"{BASE_URL}/ingredients", timeout=5)
    
    if response.status_code != 200:
        pytest.skip("Не удалось получить ингредиенты из API")
    
    data = response.json()
    if not data.get("success"):
        pytest.skip("API вернуло ошибку при запросе ингредиентов")
    
    ingredients = data.get("data", [])
    if len(ingredients) < 2:
        pytest.skip("Недостаточно ингредиентов в API")
    
    # Возвращаем ID двух первых ингредиентов
    return [ingredients[0]["_id"], ingredients[1]["_id"]]

@pytest.fixture
def invalid_ingredient_hash():
    """Фикстура для невалидного хеша ингредиента."""
    return "invalid_hash_12345"