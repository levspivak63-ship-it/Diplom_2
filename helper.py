# helper.py

import random
import string
import time

def generate_email():
    """Генерация случайного email."""
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_part}@example.com"

def generate_password():
    """Генерация случайного пароля."""
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=12))

def extract_token(response):
    """Извлечение токена из ответа."""
    return response.json().get("accessToken")

# ДОБАВЬТЕ ЭТИ ФУНКЦИИ:
def generate_random_string(length=10):
    """Генерация случайной строки из букв и цифр."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_unique_email():
    """Генерация уникального email."""
    timestamp = int(time.time())
    random_part = generate_random_string(6)
    return f"test_{timestamp}_{random_part}@example.com"

def generate_user_data():
    """Генерация данных для нового пользователя."""
    return {
        "email": generate_unique_email(),
        "password": "TestPassword123",
        "name": f"TestUser_{generate_random_string(6)}"
    }