# Feature File Example (features/api.feature)

Feature: Pet Store API Testing

  Scenario Outline: Validate all the create and update pets

    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    #POST /pet : Add a new pet
    When I send a POST request to add a pet
    Then I should receive a valid status code of <status_code> with result <reason>
#
#    #GET /pet/{petId}
    When I send a GET request for the pet by ID
    Then Pet details in GET should match
#
#    #GET /pet/findByStatus   to-do
    When I send a GET request to find a pet by <status> and <id>
#
#    #Lets check the data is the same with findByStatus
    Then Pet object should match
#
#    #PUT /pet
    Given I update the pets details with <update_catId> <update_catName> <update_name> <update_photo_url> <update_tag_id> <update_tagName> <update_status>
#
#    #Check the data is correct
#    #GET /pet/{petId}
    When I send a GET request for the pet by ID
    Then Pet details in GET should match

     #GET /pet/findByStatus
    When I send a GET request to find a pet by <update_status> and <id>
#
#    #Lets check the data is the same with findByStatus after the pet has been update
    Then Pet object should match


    Examples:
    | id                | cat_id   | cat_name               | name                   | phoUrls                      | tag_id   | tag_name       | status           | status_code | reason                | update_catId | update_catName  | update_name | update_photo_url           | update_tag_id | update_tagName | update_status |
    | 100               | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 200         | valid data            | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 100               | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | duplicate ID          | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | None              | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | missing pet ID        | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | None              | None     | None                   | None                   | None                         | None     | None           | None             | 400         | all values missing    | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | None              | 2        | None                   | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | missing category name | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | None              | 2        | danger                 | None                   | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | missing pet name      | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 1                 | 2        | danger                 | biffo                  | None                         | 1        | brute          | available        | 400         | missing photo URLs    | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 1                 | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | None     | brute          | available        | 400         | missing tag ID        | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 1                 | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | None           | available        | 400         | missing tag name      | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 1                 | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | None             | 400         | missing status        | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | -1                | -2       | danger                 | biffo                  | https://animals.com/dog.jpg  | -1       | brute          | available        | 400         | negative IDs          | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 9999999           | 2        | long_category_name     | biffoooooooooooooooo   | https://long-url-example.jpg | 1        | long_tag_name  | available        | 400         | extremely long values | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 1000000000000000  | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | extremely large ID    | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 100               | 200      | !@#$%^&*()danger       | ^&*()biffo             | https://animals.com/dog.jpg  | 300      | "brute"        | "!@#$%^&*()"     | 400         | special characters    | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 101               | 201      | cute                   | fluffy                 | not-a-valid-url              | 301      | adorable       | pending          | 400         | invalid photo URL     | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 102               | 202      | cute                   | fluffy                 | http:/invalid-url            | 302      | adorable       | available        | 400         | malformed URL         | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 103               | 203      | 'DROP TABLE pets;'     | ';DELETE FROM pets;'   | https://animals.com/hack.jpg | 303      | "'; DROP"      | available        | 400         | SQL injection attempt| 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | ""                | ""       | ""                     | ""                     | ""                           | ""       | ""             | ""               | 400         | empty strings         | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 9223372036854775807 | 2      | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | large integer values  | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 104               | 204      | friendly               | buddy                  | https://animals.com/dog.jpg  | 304      | friendly       | invalid_status   | 400         | invalid status value  | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 105               | 205      | calm                   | buddy                  | https://animals.com/dog.jpg  | 305      | calm           | SOLD             | 400         | invalid case status   | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 106               | 206      | <h1>HTML</h1>          | <script>alert("hack")</script> | https://animals.com/dog.jpg | 306 | <b>bold</b> | available | 400 | HTML injection attempt | 3 | not_dangerous | bonbon | https://animals.com/dog.jpg | 2 | cute | sold          |
    | 3.14              | 1.23     | floating_cat           | floating_name          | https://animals.com/dog.jpg  | 5.67     | floating_tag   | available        | 400         | floating-point values | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |
    | 108               | 208      | friendly               | buddy                  | https://animals.com/dog.jpg  | 308      | friendly       | AvAiLaBlE        | 400         | mixed-case status     | 3            | not_dangerous  | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |


#  Scenario: Add an invalid pet
#    Given an invalid pet payload
#    When I send a POST request with an invalid payload
#    Then the response should return 400 for invalid pet payload

#  Scenario: Get pet by valid ID
#    Given a valid pet ID
#    When I send a GET request with a valid pet ID
#    Then the response status code should be 200 and pet details should be returned

#  Scenario: Get pet by invalid ID
#    Given an invalid pet ID
#    When I send a GET request with an invalid pet ID
#    Then the response status code should be 404 for an invalid pet ID
#
#  Scenario: Delete a valid pet
#    Given a valid pet ID
#    When I send a DELETE request with a valid pet ID
#    Then the response status code should be 200 and the pet should be deleted
#
#  Scenario: Delete an invalid pet
#    Given an invalid pet ID
#    When I send a DELETE request with an invalid pet ID
#    Then the response status code should be 404 for non-existent pet
#
#  Scenario: Place an order with valid payload
#    Given a valid order payload
#    When I send a POST request to place an order
#    Then the response status code should be 200 and the order should be placed
#
#  Scenario: Place an order with invalid payload
#    Given an invalid order payload
#    When I send a POST request with an invalid order payload
#    Then the response status code should be 400 for invalid order payload
#
#  Scenario: Create a valid user
#    Given a valid user payload
#    When I send a POST request to create a new user
#    Then the response status code should be 200 and the user should be created
#
#  Scenario: Create an invalid user
#    Given an invalid user payload
#    When I send a POST request with an invalid user payload
#    Then the response status code should be 400 for invalid user payload
#
#  Scenario: User login with valid credentials
#    Given valid login credentials
#    When I send a GET request to login
#    Then the response status code should be 200 and the session should be valid
#
#  Scenario: User login with invalid credentials
#    Given invalid login credentials
#    When I send a GET request to login with invalid credentials
#    Then the response status code should be 403 for invalid credentials
#
#  Scenario: User logout
#    When I send a GET request to logout
#    Then the response status code should be 200 and the user should be logged out