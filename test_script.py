from fastapi.testclient import TestClient

from server import app

client = TestClient(app)


def test_get_form_data_with_valid_params():
    response = client.post("/get_form?field_name_1=test@mail.ru&field_name_2=%2B78005553535")
    assert response.status_code == 200
    assert response.json() == {"name": "Form template 1"}


def test_get_form_data_with_empty_params():
    response = client.post("/get_form")
    assert response.status_code == 400
    assert response.json() == {"message": "empty form, fill in params"}


def test_get_form_data_with_no_matching_params1():
    response = client.post("/get_form?field_name_4=2011-12-11")
    assert response.status_code == 200
    assert response.json() == {"field_name_4": "date"}


def test_get_form_data_with_no_matching_params2():
    response = client.post("/get_form?field_name_1=text&field_name_2=2022-12-12&field_name_3=test@email.ru")
    assert response.status_code == 200
    assert response.json() == {"name": "Form template 2"}


def test_get_form_data_with_matching_template():
    response = client.post(
        "/get_form?field_name_1=mail%40mail.ru&field_name_2=test&field_name_3=%2B78005553535&field_name_4=2022-11-20")
    assert response.status_code == 200
    assert response.json() == {"name": "Form template 3"}
