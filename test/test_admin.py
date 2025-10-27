import requests
import pytest

BASE_URL = "http://localhost:8000/api"

def test_get_administradores_success():
    response = requests.get(f"{BASE_URL}/administrador/")
    assert response.status_code == 200
    administradores = response.json()
    assert isinstance(administradores, list)
    assert len(administradores) >= 0

def test_get_administrador_por_id():
    """Consulta un administrador específico por ID"""
    id = 30  # Cambia este ID según los datos que tengas en la base
    response = requests.get(f"{BASE_URL}/administrador/{id}")
    assert response.status_code == 200, f"Error: código {response.status_code}"
    
    admin = response.json()
    assert 'username' in admin, "La respuesta no contiene 'username'"
    assert admin['username'] == "solosena2025@gmail.com" 
