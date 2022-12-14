import pytest
import requests
import time
import redis
from settings import REDIS_PORT, APPLICATION_PORT

def test_system_happy_path():
    response = requests.post(f"http://localhost:{APPLICATION_PORT}/api/image/validate", json={
        "assetPath": { 
            "location": "local",
            "path": "./files/valid-image.jpg"
        },
        "notifications": {
            "onStart": "https://google.com",
            "onSuccess": "https://google.com",
            "onFailure": "https://google.com"
        }
    })

    assert response.status_code == 200

    time.sleep(5)

    log_file = open("application.log", "r").readlines()
    assert "Notifying success to client" in log_file[-3]
    # checking for method not allowed, in the future we should have a valid endpoint to test client side
    assert "- 405" in log_file[-3]
    assert "succeeded" in log_file[-2]

def test_system_invalid_notification_url():
    response = requests.post(f"http://localhost:{APPLICATION_PORT}/api/image/validate", json={
        "assetPath": { 
            "location": "local",
            "path": "./files/valid-image.jpg"
        },
        "notifications": {
            "onStart": "https://google.com",
            "onSuccess": "https://google.com",
            "onFailure": "invalid-url"
        }
    })

    assert response.status_code == 400
    assert response.text == "{\"errors\": [{\"onFailure\": \"URL is invalid\"}]}"

def test_get_image_processing_status():
        redis_utility = redis.Redis(host="localhost", port=REDIS_PORT, db=0)

        redis_utility.set("1", "complete", ex=3)

        response = requests.get(f"http://localhost:{APPLICATION_PORT}/api/assets?id=1")

        assert response.status_code == 200
        assert response.text == "complete"

        # Test expiration
        time.sleep(4)

        response = requests.get(f"http://localhost:{APPLICATION_PORT}/api/assets?id=1")

        assert response.status_code == 204

