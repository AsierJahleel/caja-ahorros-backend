import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"mensaje": "Sistema de Gestión de Caja de Ahorros activo"}

def test_crear_socio():
    payload = {"nombre": "Asier Test", "cedula": "0999999999", "saldo": 100.0}
    response = client.post("/socios/", json=payload)
    assert response.status_code == 200
    assert response.json()["cedula"] == "0999999999"