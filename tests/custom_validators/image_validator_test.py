import pytest
from crawlers import image_crawler
from custom_validators import image_validator

@pytest.fixture()
def input_data():
    return {
        "assetPath": { 
            "location": "local",
            "path": "./files/valid-image.jpg",
        }
    }

@pytest.mark.parametrize(
    "path,expected_response_is_valid,expected_response_errors",
    [
        pytest.param("./files/valid-image.jpg", True, "{'errors': []}", id="local-valid"),
        pytest.param("./files/invalid-image.gif", False, "{'errors': [{'format': \"Only ['jpeg'] are formats supported\"}]}", id="local-invalid-gif"),
        pytest.param("./files/invalid-image.jpg", False, "{'errors': [{'dimension': 'Height and width must not be greater than 1000 and 1000'}]}", id="local-invalid-size"),
    ],
)
def test_validate(input_data, path, expected_response_is_valid, expected_response_errors):
    input_data["assetPath"]["path"] = path
    
    response = image_crawler.crawl(input_data["assetPath"])
    response = image_validator.validate(response.object)

    assert response.is_valid == expected_response_is_valid
    assert expected_response_errors in str(response.object)