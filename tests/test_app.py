# tests/test_app.py


def test_health(client, monkeypatch):
    monkeypatch.delenv("APP_VERSION", raising=False)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "local"}


def test_health_deployed_version(client, monkeypatch):
    monkeypatch.setenv("APP_VERSION", "version-de-prueba")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "version-de-prueba"}


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert (
        b"<!DOCTYPE html>" in response.data
    )  # Assuming the HTML template starts with <!DOCTYPE html>


def test_index_post_sumar(post_form):
    response = post_form(data={"num1": "2", "num2": "3", "operacion": "sumar"})
    assert response.status_code == 200
    assert b"Resultado: 5.0" in response.data


def test_index_post_restar(post_form):
    response = post_form(data={"num1": "5", "num2": "3", "operacion": "restar"})
    assert response.status_code == 200
    assert b"Resultado: 2.0" in response.data


def test_index_post_multiplicar(post_form):
    response = post_form(data={"num1": "2", "num2": "3", "operacion": "multiplicar"})
    assert response.status_code == 200
    assert b"Resultado: 6.0" in response.data


def test_index_post_dividir(post_form):
    response = post_form(data={"num1": "6", "num2": "3", "operacion": "dividir"})
    assert response.status_code == 200
    assert b"Resultado: 2.0" in response.data


def test_index_post_dividir_by_zero(post_form):
    response = post_form(data={"num1": "6", "num2": "0", "operacion": "dividir"})
    assert response.status_code == 200
    assert b"Error: No se puede dividir por cero" in response.data


def test_index_post_invalid_operation(post_form):
    response = post_form(data={"num1": "6", "num2": "3", "operacion": "invalid"})
    assert response.status_code == 200
    assert b"Operaci\xc3\xb3n no v\xc3\xa1lida" in response.data


def test_index_post_invalid_numbers(post_form):
    response = post_form(data={"num1": "a", "num2": "b", "operacion": "sumar"})
    assert response.status_code == 200
    assert b"Error: Introduce n\xc3\xbameros v\xc3\xa1lidos" in response.data
