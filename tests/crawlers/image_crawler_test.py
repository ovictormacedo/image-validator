import pytest
from crawlers import image_crawler

@pytest.fixture()
def input_data():
    return {
        "assetPath": { 
            "location": "local",
            "path": "./files/valid-image.jpg",
        }
    }

@pytest.mark.parametrize(
    "path,expected_response",
    [
        pytest.param("./files/valid-image.jpg", "success", id="local-valid"),
        pytest.param("./files/validimage.jpg", "FileNotFound", id="local-notfound"),
        pytest.param("./files", "ThePathIsADirectory", id="local-directory"),
    ],
)
def test_image_crawler(input_data, path, expected_response):
    input_data["assetPath"]["path"] = path
    
    response = image_crawler.crawl(input_data["assetPath"])

    assert response.status == expected_response
    