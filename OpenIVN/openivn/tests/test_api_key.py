"""Tests API key authentication."""
import requests


def test_api_key_success():
    """Tests using a valid API key."""
    url = "http://localhost:1609/api/v1/hello_world/"
    headers = {
        'x-api-key': 'd1bd8f540e3f5c90c7d960ec9d1465273094bba20064cd1ab71fdf3aea9f2639bfcfca45742b62ab5b3e6fad53d0e4fb054c072d4504300d78544b1802336c3b'
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200


def test_api_key_unauthorized():
    """Tests using an invalid API key."""
    url = "http://localhost:1609/api/v1/hello_world/"
    response = requests.get(url)
    assert response.status_code == 401


if __name__ == '__main__':
    test_api_key_success()
    test_api_key_unauthorized()
