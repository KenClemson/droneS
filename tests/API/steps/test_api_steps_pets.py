# Pytest BDD Tests for Swagger Pet Store API
# Test Suite Structure: Implementing BDD (Gherkin Style) for the Pet Store API

# Required Imports
import requests
import pytest
from requests.exceptions import RequestException
from pytest_bdd import scenarios, given, when, then, parsers
import json
import logging

# Base URL for the API
BASE_URL = "https://petstore.swagger.io/v2"

# Load scenarios from feature files
scenarios("/app/tests/API/features/pets.feature")

# ------------------------------------
# PET ENDPOINT TESTS
# ------------------------------------
def convert_to_none_or_int(value):
    if value == "None":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

@given(parsers.parse("a valid pet payload with {id} {cat_id} {cat_name} {name} {phoUrls} {tag_id} {tag_name} {status}"))
def valid_pet_payload(context, id, cat_id,
                      cat_name, name, phoUrls,
                      tag_id, tag_name, status):
    """Creates a valid pet payload with None-handling and safe type conversion."""

    payload = {
        "id": convert_to_none_or_int(id),
        "category": {
            "id": convert_to_none_or_int(cat_id),
            "name": cat_name if cat_name != "None" else None
        },
        "name": name if name != "None" else None,
        "photoUrls": [phoUrls] if phoUrls and phoUrls != "None" else [],
        "tags": [
            {
                "id": convert_to_none_or_int(tag_id),
                "name": tag_name if tag_name != "None" else None
            }
        ] if tag_id and tag_name else [],
        "status": status if status != "None" else None
    }
    context["payload"] = payload



@given(parsers.parse("I update the pets details with {update_catId} {update_catName} {update_name} {update_photo_url} {update_tag_id} {update_tagName} {update_status}"))
def update_pet_payload(context, update_catId, update_catName, update_name,
                       update_photo_url, update_tag_id,
                       update_tagName, update_status):
    """
    Updates the pet payload in the context with new values for the PUT request.
    Handles None values and converts types safely.
    """
    # Get the current payload
    payload = context["payload"]
    # Update the payload with new values
    payload["category"] = {
        "id": convert_to_none_or_int(update_catId),
        "name": update_catName if update_catName != "None" else None
    }
    payload["name"] = update_name if update_name != "None" else None
    payload["photoUrls"] = [update_photo_url] if update_photo_url != "None" else []
    payload["tags"] = [{
        "id": convert_to_none_or_int(update_tag_id),
        "name": update_tagName if update_tagName != "None" else None
    }] if update_tag_id != "None" and update_tagName != "None" else []
    payload["status"] = update_status if update_status != "None" else None

    # Save the updated payload back to the context
    logging.info(f"Updated payload: {payload}")
    context["payload"] = payload
    try:
        payload = context["payload"]
        response = requests.put(f"{BASE_URL}/pet", json=payload)
        context["response"] = response  # Store the response in context
        logging.info(f"Updated Response Status Code: {response.status_code}")
        try:
            logging.info(f"Updated Response JSON: {json.dumps(response.json(), indent=4)}")
        except json.JSONDecodeError:
            logging.warning(f"Response is not JSON: {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        context["payload"] = None
        raise


@when("I send a POST request to add a pet")
def post_pet(context):
    try:
        payload = context["payload"]
        response = requests.post(f"{BASE_URL}/pet", json=payload)
        context["response"] = response  # Store the response in context
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        context["response"] = None
        raise


@then(parsers.parse("I should receive a valid status code of {status_code} with result {reason}"))
def validate_status_code(context, status_code, reason):
    """Validate the response status code and skip the scenario if it doesn't match."""
    response = context["response"]
    expected_status_code = int(status_code)

    if response.status_code != expected_status_code:
        pytest.fail(
            f"Failing due to {reason}. Expected {expected_status_code}, but got {response.status_code}.")

    assert response.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, got {response.status_code}"
    )

@when("I send a GET request for the pet by ID")
def get_pet_by_id(context):
    """Sends a GET request to retrieve the pet by ID."""
    pet_id = context["payload"]["id"]
    response = requests.get(f"{BASE_URL}/pet/{pet_id}")
    context["get_response"] = response  # Store the GET response in context
    logging.info(f"GET Response Status Code: {response.status_code}")
    try:
        logging.info(f"GET Response JSON: {json.dumps(response.json(), indent=4)}")
    except json.JSONDecodeError:
        logging.warning(f"GET Response is not JSON: {response.text}")

@when(parsers.parse("I send a GET request to find a pet by {status} and {id}"))
def get_pet_by_id(status, id, context):
    """
    Sends a GET request to retrieve the pet by ID and status.
    """
    # Validate inputs
    assert isinstance(status, str), "Status must be a string."
    assert id.isdigit(), "ID must be an integer string."

    # Convert `id` to integer for comparison
    id = int(id)

    try:
        # Send GET request
        response = requests.get(f"{BASE_URL}/pet/findByStatus?status={status}")
        response.raise_for_status()  # Ensure a successful status code
        response_json = response.json()

        # Check if the response is an array
        assert isinstance(response_json, list), "Response is not an array."

        # Search for the pet by ID
        pet = next((item for item in response_json if item["id"] == id), None)

        # Update context if pet is found
        if pet:
            context["get_response"] = pet
            logging.info(f"Found pet: {json.dumps(pet, indent=4)}")
        else:
            logging.warning(f"No pet found with ID {id} and status '{status}'.")

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP request failed: {e}")

    except AssertionError as e:
        logging.error(f"Validation error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

@then("Pet details in GET should match")
def verify_pet_details(context):
    """Verifies that the GET response contains the same values as the payload."""
    get_response = context["get_response"]
    assert get_response.status_code == 200, f"Expected 200 but got {get_response.status_code}"

    # Parse the GET response JSON
    response_json = get_response.json()
    payload = context["payload"]

    # Verify all keys match
    assert response_json.get("id") == payload.get("id"), f"ID mismatch: {response_json.get('id')} vs {payload.get('id')}"

    # Category verification
    assert "category" in response_json, "Category is missing in the response."
    assert "category" in payload, "Category is missing in the payload."
    category_response = response_json["category"]
    category_payload = payload["category"]

    assert category_response.get("id") == category_payload.get("id"), f"Category ID mismatch: {category_response.get('id')} vs {category_payload.get('id')}"
    assert category_response.get("name") == category_payload.get("name"), f"Category name mismatch: {category_response.get('name')} vs {category_payload.get('name')}"

    # Name verification
    assert response_json.get("name") == payload.get("name"), f"Name mismatch: {response_json.get('name')} vs {payload.get('name')}"

    # Photo URLs verification
    response_photo_urls = response_json.get("photoUrls", [])
    payload_photo_urls = payload.get("photoUrls", [])
    assert response_photo_urls == payload_photo_urls, f"Photo URL mismatch: {response_photo_urls} vs {payload_photo_urls}"

    # Tags verification
    response_tags = response_json.get("tags", [])
    payload_tags = payload.get("tags", [])

    if response_tags and payload_tags:
        assert response_tags[0].get("id") == payload_tags[0].get("id"), f"Tag ID mismatch: {response_tags[0].get('id')} vs {payload_tags[0].get('id')}"
        assert response_tags[0].get("name") == payload_tags[0].get("name"), f"Tag name mismatch: {response_tags[0].get('name')} vs {payload_tags[0].get('name')}"
    else:
        assert not response_tags and not payload_tags, f"Tags mismatch: {response_tags} vs {payload_tags}"

    # Status verification
    assert response_json.get("status") == payload.get("status"), f"Status mismatch: {response_json.get('status')} vs {payload.get('status')}"

    print("All fields in the GET response match the original POST payload!")

@then("Pet object should match")
def verify_pet_object(context):
    """Verifies that the pet object contains the same values as the original create pet payload."""
    pet = context["get_response"]
    payload = context["payload"]

    # Verify all keys match
    assert pet.get("id") == payload.get("id"), f"ID mismatch: {pet.get('id')} vs {payload.get('id')}"

    # Category verification
    assert "category" in pet, "Category is missing in the response."
    assert "category" in payload, "Category is missing in the payload."
    category_response = pet["category"]
    category_payload = payload["category"]

    assert category_response.get("id") == category_payload.get("id"), f"Category ID mismatch: {category_response.get('id')} vs {category_payload.get('id')}"
    assert category_response.get("name") == category_payload.get("name"), f"Category name mismatch: {category_response.get('name')} vs {category_payload.get('name')}"

    # Name verification
    assert pet.get("name") == payload.get("name"), f"Name mismatch: {pet.get('name')} vs {payload.get('name')}"

    # Photo URLs verification
    response_photo_urls = pet.get("photoUrls", [])
    payload_photo_urls = payload.get("photoUrls", [])
    assert response_photo_urls == payload_photo_urls, f"Photo URL mismatch: {response_photo_urls} vs {payload_photo_urls}"

    # Tags verification
    response_tags = pet.get("tags", [])
    payload_tags = payload.get("tags", [])

    if response_tags and payload_tags:
        assert response_tags[0].get("id") == payload_tags[0].get("id"), f"Tag ID mismatch: {response_tags[0].get('id')} vs {payload_tags[0].get('id')}"
        assert response_tags[0].get("name") == payload_tags[0].get("name"), f"Tag name mismatch: {response_tags[0].get('name')} vs {payload_tags[0].get('name')}"
    else:
        assert not response_tags and not payload_tags, f"Tags mismatch: {response_tags} vs {payload_tags}"

    # Status verification
    assert pet.get("status") == payload.get("status"), f"Status mismatch: {pet.get('status')} vs {payload.get('status')}"

    logging.info("All fields in the pet object match the original POST payload!")



# ------------------------------------
# GET PET BY ID
# ------------------------------------
@given("a valid pet ID")
def valid_pet_id():
    return 1

@given("an invalid pet ID")
def invalid_pet_id():
    return "invalid_id"

@when("I send a GET request with a valid pet ID")
def get_pet_by_id(valid_pet_id):
    try:
        response = requests.get(f"{BASE_URL}/pet/{valid_pet_id}")
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@when("I send a GET request with an invalid pet ID")
def get_pet_by_invalid_id(invalid_pet_id):
    try:
        response = requests.get(f"{BASE_URL}/pet/{invalid_pet_id}")
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@then("the response status code should be 200 and pet details should be returned")
def verify_pet_by_id(get_pet_by_id):
    assert get_pet_by_id.status_code == 200
    assert "name" in get_pet_by_id.json()

@then("the response status code should be 404 for an invalid pet ID")
def verify_pet_not_found(get_pet_by_invalid_id):
    assert get_pet_by_invalid_id.status_code == 404


# ------------------------------------
# DELETE PET
# ------------------------------------
@when("I send a DELETE request with a valid pet ID")
def delete_pet(valid_pet_id):
    try:
        response = requests.delete(f"{BASE_URL}/pet/{valid_pet_id}")
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@when("I send a DELETE request with an invalid pet ID")
def delete_invalid_pet():
    try:
        response = requests.delete(f"{BASE_URL}/pet/invalid_id")
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@then("the response status code should be 200 and the pet should be deleted")
def verify_pet_deleted(delete_pet):
    assert delete_pet.status_code == 200

@then("the response status code should be 404 for non-existent pet")
def verify_pet_delete_failure(delete_invalid_pet):
    assert delete_invalid_pet.status_code == 404


# ------------------------------------
# STORE ENDPOINT TESTS
# ------------------------------------
@given("a valid order payload")
def valid_order_payload():
    return {
        "id": 10,
        "petId": 1,
        "quantity": 2,
        "shipDate": "2025-01-01T10:00:00.000Z",
        "status": "placed",
        "complete": True
    }

@given("an invalid order payload")
def invalid_order_payload():
    return {
        "id": "invalid_id",
        "petId": -1,
        "quantity": "two",
        "status": "invalid"
    }

@when("I send a POST request to place an order")
def place_order(valid_order_payload):
    try:
        response = requests.post(f"{BASE_URL}/store/order", json=valid_order_payload)
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@when("I send a POST request with an invalid order payload")
def place_invalid_order(invalid_order_payload):
    try:
        response = requests.post(f"{BASE_URL}/store/order", json=invalid_order_payload)
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@then("the response status code should be 200 and the order should be placed")
def verify_order_placed(place_order):
    assert place_order.status_code == 200

@then("the response status code should be 400 for invalid order payload")
def verify_invalid_order(place_invalid_order):
    assert place_invalid_order.status_code == 400


# ------------------------------------
# USER ENDPOINT TESTS
# ------------------------------------
@given("a valid user payload")
def valid_user_payload():
    return {
        "id": 100,
        "username": "testuser",
        "firstName": "John",
        "lastName": "Doe",
        "email": "testuser@example.com",
        "password": "password123",
        "phone": "1234567890",
        "userStatus": 1
    }

@given("an invalid user payload")
def invalid_user_payload():
    return {
        "username": "",
        "password": "short"
    }

@when("I send a POST request to create a new user")
def create_user(valid_user_payload):
    try:
        response = requests.post(f"{BASE_URL}/user", json=valid_user_payload)
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@when("I send a POST request with an invalid user payload")
def create_invalid_user(invalid_user_payload):
    try:
        response = requests.post(f"{BASE_URL}/user", json=invalid_user_payload)
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@then("the response status code should be 200 and the user should be created")
def verify_user_created(create_user):
    assert create_user.status_code == 200

@then("the response status code should be 400 for invalid user payload")
def verify_invalid_user_created(create_invalid_user):
    assert create_invalid_user.status_code == 400


# ------------------------------------
# USER LOGIN AND LOGOUT
# ------------------------------------
@given("valid login credentials")
def valid_login_credentials():
    return {"username": "testuser", "password": "password123"}

@given("invalid login credentials")
def invalid_login_credentials():
    return {"username": "invaliduser", "password": "wrongpass"}

@when("I send a GET request to login")
def login_user(valid_login_credentials):
    try:
        params = {"username": valid_login_credentials["username"], "password": valid_login_credentials["password"]}
        response = requests.get(f"{BASE_URL}/user/login", params=params)
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@when("I send a GET request to login with invalid credentials")
def login_invalid_user(invalid_login_credentials):
    try:
        params = {"username": invalid_login_credentials["username"], "password": invalid_login_credentials["password"]}
        response = requests.get(f"{BASE_URL}/user/login", params=params)
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@then("the response status code should be 200 and the session should be valid")
def verify_user_logged_in(login_user):
    assert login_user.status_code == 200
    assert "message" in login_user.json()

@then("the response status code should be 403 for invalid credentials")
def verify_invalid_login(login_invalid_user):
    assert login_invalid_user.status_code == 403

@when("I send a GET request to logout")
def logout_user():
    try:
        response = requests.get(f"{BASE_URL}/user/logout")
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response

@then("the response status code should be 200 and the user should be logged out")
def verify_user_logged_out(logout_user):
    assert logout_user.status_code == 200