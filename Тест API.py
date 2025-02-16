import requests
import pytest
import random

BASE_URL = "https://qa-internship.avito.com"

@pytest.fixture
def unique_seller_id():
    return random.randint(111111, 999999)

@pytest.fixture
def create_listing(unique_seller_id):
    payload = {
        "title": "Test Ad",
        "description": "This is a test listing",
        "price": 1000,
        "sellerID": unique_seller_id
    }
    response = requests.post(f"{BASE_URL}/ad", json=payload)
    assert response.status_code == 201
    return response.json()["id"]

# Test creating a listing
def test_create_listing(unique_seller_id):
    payload = {
        "title": "Test Ad",
        "description": "This is a test listing",
        "price": 1000,
        "sellerID": unique_seller_id
    }
    response = requests.post(f"{BASE_URL}/ad", json=payload)
    assert response.status_code == 201
    assert "id" in response.json()

# Test retrieving a listing
def test_get_listing_by_id(create_listing):
    response = requests.get(f"{BASE_URL}/ad/{create_listing}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ad"

# Test retrieving non-existing listing
def test_get_non_existing_listing():
    response = requests.get(f"{BASE_URL}/ad/999999999")
    assert response.status_code == 404

# Test retrieving listings by seller ID
def test_get_listings_by_seller_id(unique_seller_id):
    response = requests.get(f"{BASE_URL}/ads/{unique_seller_id}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test retrieving statistics
def test_get_item_statistics(create_listing):
    response = requests.get(f"{BASE_URL}/stats/{create_listing}")
    assert response.status_code == 200
    assert "views" in response.json()

# Test retrieving statistics for non-existing item
def test_get_non_existing_statistics():
    response = requests.get(f"{BASE_URL}/stats/999999999")
    assert response.status_code == 404