import pytest
from custom_validators import image_validator_controller_input_validator

@pytest.fixture(autouse=True)
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

def test_validate_incorrect_schema(input_data):
    input_data["notifications"].pop("onStart", None)

    response = image_validator_controller_input_validator.validate(input_data)

    assert response.is_valid == False
    assert str(response.object) == "{'errors': {'notifications': {'onStart': ['Missing data for required field.']}}}"

@pytest.mark.parametrize(
    "incorrect_url_attribute,expected_response_errors",
    [
        pytest.param("onStart", "{'errors': [{'onStart': 'URL is invalid'}]}", id="invalid-onStart"),
        pytest.param("onFailure", "{'errors': [{'onFailure': 'URL is invalid'}]}", id="invalid-onFailure"),
        pytest.param("onSuccess", "{'errors': [{'onSuccess': 'URL is invalid'}]}", id="invalid-onSuccess"),
    ],
)
def test_validate_invalid_notification_url(input_data, incorrect_url_attribute, expected_response_errors):
    input_data["notifications"][incorrect_url_attribute] = "any-invalid-url"

    response = image_validator_controller_input_validator.validate(input_data)

    assert response.is_valid == False
    assert str(response.object) == expected_response_errors

def test_validate(input_data):
    response = image_validator_controller_input_validator.validate(input_data)

    assert response.is_valid == True
    assert response.object == input_data