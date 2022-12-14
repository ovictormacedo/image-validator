import pytest
import main
from unittest import mock

def redis_get_override(self, key):
    if key == "1":
        return "complete"
    else:
        return None

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
    "id,expected_status,expected_message",
    [
        pytest.param("", 400, "Please inform an asset id", id="missing-id"),
        pytest.param(2, 204, "", id="id-not-found"),
        pytest.param(1, 200, "complete", id="id-found"),
    ],
)
def test_get_image_processing_status(client, id, expected_status, expected_message):
    with mock.patch("utilities.redis_utility.redis.Redis.get", new=redis_get_override):
        response = client.get(f"/api/assets?id={id}")

    assert response.status_code == expected_status
    assert response.text == expected_message