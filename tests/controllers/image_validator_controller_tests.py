import pytest
import main
from unittest import mock

@pytest.fixture()
def input_data():
    return {
        "assetPath": { 
            "location": "local",
            "path": "./files/valid-image.jpg",
        },
        "notifications": {
            "onStart": "http://somevalidurl.com",
            "onSuccess": "http://somevalidurl.com",
            "onFailure": "http://somevalidurl.com"
        }
    }

@pytest.fixture()
def app():
    app = main.main_app
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.mark.parametrize(
    "invalid_field,expected_status_code,expected_response",
    [
        pytest.param("", 200, "Success", id="success"),
        pytest.param("onStart", 400, "{\"errors\": [{\"onStart\": \"URL is invalid\"}]}", id="missing onStart"),
        pytest.param("onSuccess", 400, "{\"errors\": [{\"onSuccess\": \"URL is invalid\"}]}", id="missing onSuccess"),
        pytest.param("onFailure", 400, "{\"errors\": [{\"onFailure\": \"URL is invalid\"}]}", id="missing onFailure"),
    ],
)
def test_image_validator_controller(client, input_data, invalid_field, expected_status_code, expected_response):    
    if invalid_field != "":
        input_data["notifications"][invalid_field] = ""

    request_mock = mock.MagicMock()
    request_mock.status_code = 200
    with mock.patch("utilities.client_notification_utility.requests.post", request_mock),\
        mock.patch("utilities.celery_utility.Celery.send_task", request_mock),\
        mock.patch("utilities.redis_utility.redis.Redis.set", request_mock):
        response = client.post("/api/image/validate", json=input_data)

    assert response.status_code == expected_status_code
    assert expected_response in response.text