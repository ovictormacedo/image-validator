import pytest
from unittest import mock
from tasks import image_validator_task

@pytest.fixture()
def input_data():
    return {
        "id": "assetId",
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

@pytest.mark.parametrize(
    "path,location,expected_response",
    [
        pytest.param("./files/valid-image.jpg", "local", True, id="local-success"),
        pytest.param("./files/invalid-image.jpg", "local", False, id="local-invalid"),
        pytest.param("./files/validimage.jpg", "local", False, id="local-notfound"),
        pytest.param("./files/valid-image.gif", "local", False, id="local-invalid-format"),
        pytest.param("./files", "local", False, id="local-directory"),
    ],
)
def test_image_validator_task(input_data, path, location, expected_response):
    input_data["assetPath"]["path"] = path
    input_data["assetPath"]["location"] = location

    request_mock = mock.MagicMock()
    request_mock.status_code = 200
    with mock.patch("utilities.client_notification_utility.requests.post", request_mock),\
        mock.patch("utilities.celery_utility.Celery.send_task", request_mock),\
        mock.patch("utilities.redis_utility.redis.Redis.set", request_mock):
        response = image_validator_task.validate_image(input_data)

    assert response == expected_response