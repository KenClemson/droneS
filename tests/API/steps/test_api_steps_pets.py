# Pytest BDD Tests for Swagger Pet Store API
# Test Suite Structure: Implementing BDD (Gherkin Style) for the Pet Store API

# Required Imports
import requests
import pytest
from requests.exceptions import RequestException
from pytest_bdd import scenarios, given, when, then, parsers
import json
import logging
from tests.config_loader import load_config

# Base URL for the API
#BASE_URL = "https://petstore.swagger.io/v2"
config = load_config()
BASE_URL = config["API_BASE_URL"]

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
        validate_response_headers(response)
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
    validate_response_headers(response)
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
        validate_response_headers(response)
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


@when(parsers.parse("I send a DELETE request with a valid pet {id}"))
def delete_pet(context, id):
    try:
        response = requests.delete(f"{BASE_URL}/pet/{id}")
        context["response"] = response
        logging.info(f"Found deleted: {response}")
        response.raise_for_status()
    except RequestException as e:
        return e.response
    return response


@then("the response status code should be 200 and the pet should be deleted")
def verify_pet_deleted(context):
    response = context["response"]
    expected_message = "Pet not found"

    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

    try:
        response_json = response.json()
        logging.info(f"Response JSON: {json.dumps(response_json, indent=4)}")
        actual_message = response_json.get("message", "No message found")
        assert actual_message == expected_message, f"Expected '{expected_message}', but got '{actual_message}'"
    except json.JSONDecodeError:
        pytest.fail("Response body is not valid JSON")

def validate_response_headers(response, expected_headers=None):
    """
    Validates that the response contains the expected headers.
    If `expected_headers` is None, default common headers are checked.
    We need to find out from the dev team what headers are expected.
    """
    # Log the full headers for visibility
    logging.info(f"Response Headers: {json.dumps(dict(response.headers), indent=4)}")

    if expected_headers is None:
        expected_headers = {
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }

    for header, expected_value in expected_headers.items():
        assert header in response.headers, f"Header '{header}' is missing!"
        actual_value = response.headers.get(header)
        assert actual_value == expected_value, f"Header '{header}' value mismatch! Expected: {expected_value}, but got: {actual_value}"


