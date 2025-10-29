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

def test_post_agregar_administrador():
    nuevo_admin = {
        "first_name": "admin_test",
        "last_name": "2010-01-01",
        "email": "example@gmail.com",
        "fecha_nacimiento": "2000-01-01",
    }
    response2=requests.get(f"{BASE_URL}/administrador/")
    longitud_inicial=len(response2.json())
    response = requests.post(f"{BASE_URL}/administrador/", json=nuevo_admin)
    response3=requests.get(f"{BASE_URL}/administrador/")
    assert response.status_code == 201
    assert response2.status_code==200
    assert len(response3.json())>longitud_inicial
    
def test_put_actualizar_administrador():
    
    response = requests.get(f"{BASE_URL}/administrador/")
    admins = response.json()
    admin_test = next((a for a in admins if a["first_name"] == "admin_test"), None)

    admin_id = admin_test["id"]
    admin_actualizado = {
        "first_name": "admin_updated",
        "last_name": "updated_lastname",
        "email": "exampleupdate@gmail.com",
        "fecha_nacimiento": "1995-05-05",
    }
    response = requests.put(f"{BASE_URL}/administrador/{admin_id}", json=admin_actualizado)
    assert response.status_code == 200
    admin = response.json()
    assert admin['first_name'] == "admin_updated"
    
def test_delete_administrador():
    response = requests.get(f"{BASE_URL}/administrador/")
    assert response.status_code == 200

    admins = response.json()
    admin_test = next((a for a in admins if a["first_name"] == "admin_updated"), None)

    admin_id = admin_test["id"]

    delete_response = requests.delete(f"{BASE_URL}/administrador/{admin_id}")
    assert delete_response.status_code in (200, 204), f"Código inesperado: {delete_response.status_code}"

    get_response = requests.get(f"{BASE_URL}/administrador/{admin_id}")
    assert get_response.status_code == 404
