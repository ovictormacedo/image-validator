import pytest
from custom_validators import url_validator

@pytest.mark.parametrize(
    "url,expected_response",
    [
        pytest.param("https://google.com", True, id="valid-url"),
        pytest.param("any-invalid-url", False, id="invalid-url"),
    ],
)
def test_is_valid_url(url, expected_response):
    response = url_validator.is_valid_url(url)

    assert response == expected_response