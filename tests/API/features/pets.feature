
Feature: Pet Store API Testing

  # Scenario Outline for POST /pet
  Scenario Outline: Add a pet (POST /pet)
    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    When I send a POST request to add a pet
    Then I should receive a valid status code of <status_code> with result <reason>
  Examples:
    | id  | cat_id | cat_name | name   | phoUrls                      | tag_id | tag_name | status    | status_code | reason     |
    | 100 | 2      | danger   | biffo  | https://animals.com/dog.jpg  | 1      | brute    | available | 200         | valid data |


  # Scenario Outline for GET /pet/{petId}
  Scenario Outline: Get a pet by ID (GET /pet/{petId})
    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    When I send a POST request to add a pet
    When I send a GET request for the pet by ID
    Then Pet details in GET should match
  Examples:
    | id  | cat_id | cat_name | name   | phoUrls                      | tag_id | tag_name | status    |
    | 100 | 2      | danger   | biffo  | https://animals.com/dog.jpg  | 1      | brute    | available |


  # Scenario Outline for GET /pet/findByStatus
  Scenario Outline: Get a pet by status (GET /pet/findByStatus)
    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    When I send a POST request to add a pet
    When I send a GET request to find a pet by <status> and <id>
    Then Pet object should match
  Examples:
    | id  | cat_id | cat_name | name   | phoUrls                      | tag_id | tag_name | status    |
    | 100 | 2      | danger   | biffo  | https://animals.com/dog.jpg  | 1      | brute    | available |


  # Scenario Outline for PUT /pet
  Scenario Outline: Update a pet (PUT /pet)
    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    When I send a POST request to add a pet
    Given I update the pets details with <update_catId> <update_catName> <update_name> <update_photo_url> <update_tag_id> <update_tagName> <update_status>
    When I send a GET request for the pet by ID
    Then Pet details in GET should match
  Examples:
    | id  | cat_id | cat_name | name   | phoUrls                      | tag_id | tag_name | status     | update_catId | update_catName | update_name | update_photo_url           | update_tag_id | update_tagName | update_status |
    | 100 | 2      | danger   | biffo  | https://animals.com/dog.jpg  | 1      | brute    | available  | 3            | not_dangerous | bonbon      | https://animals.com/dog.jpg | 2             | cute          | sold          |


  # Scenario Outline for DELETE /pet
  Scenario Outline: Delete a pet (DELETE /pet)
    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    When I send a POST request to add a pet
    When I send a DELETE request with a valid pet <id>
    Then the response status code should be 200 and the pet should be deleted
    When I send a GET request for the pet by ID
    Then I should see the error message "Pet not found"

  Examples:
    | id  | cat_id | cat_name | name   | phoUrls                      | tag_id | tag_name | status    |
    | 100 | 2      | danger   | biffo  | https://animals.com/dog.jpg  | 1      | brute    | available |


  Scenario Outline: Validate incorrect data

    Given a valid pet payload with <id> <cat_id> <cat_name> <name> <phoUrls> <tag_id> <tag_name> <status>
    When I send a POST request to add a pet
    Then I should receive a valid status code of <status_code> with result <reason>


    Examples:
    | id                | cat_id   | cat_name               | name                   | phoUrls                      | tag_id   | tag_name       | status           | status_code | reason                |
    | 100               | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 200         | valid data            |
    | 100               | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | duplicate ID          |
    | None              | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | missing pet ID        |
    | None              | None     | None                   | None                   | None                         | None     | None           | None             | 400         | all values missing    |
    | None              | 2        | None                   | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | missing category name |
    | None              | 2        | danger                 | None                   | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | missing pet name      |
    | 1                 | 2        | danger                 | biffo                  | None                         | 1        | brute          | available        | 400         | missing photo URLs    |
    | 1                 | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | None     | brute          | available        | 400         | missing tag ID        |
    | 1                 | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | None           | available        | 400         | missing tag name      |
    | 1                 | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | None             | 400         | missing status        |
    | -1                | -2       | danger                 | biffo                  | https://animals.com/dog.jpg  | -1       | brute          | available        | 400         | negative IDs          |
    | 9999999           | 2        | long_category_name     | biffoooooooooooooooo   | https://long-url-example.jpg | 1        | long_tag_name  | available        | 400         | extremely long values |
    | 1000000000000000  | 2        | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | extremely large ID    |
    | 100               | 200      | !@#$%^&*()danger       | ^&*()biffo             | https://animals.com/dog.jpg  | 300      | "brute"        | "!@#$%^&*()"     | 400         | special characters    |
    | 101               | 201      | cute                   | fluffy                 | not-a-valid-url              | 301      | adorable       | pending          | 400         | invalid photo URL     |
    | 102               | 202      | cute                   | fluffy                 | http:/invalid-url            | 302      | adorable       | available        | 400         | malformed URL         |
    | 103               | 203      | 'DROP TABLE pets;'     | ';DELETE FROM pets;'   | https://animals.com/hack.jpg | 303      | "'; DROP"      | available        | 400         | SQL injection attempt|
    | ""                | ""       | ""                     | ""                     | ""                           | ""       | ""             | ""               | 400         | empty strings         |
    | 9223372036854775807 | 2      | danger                 | biffo                  | https://animals.com/dog.jpg  | 1        | brute          | available        | 400         | large integer values  |
    | 104               | 204      | friendly               | buddy                  | https://animals.com/dog.jpg  | 304      | friendly       | invalid_status   | 400         | invalid status value  |
    | 105               | 205      | calm                   | buddy                  | https://animals.com/dog.jpg  | 305      | calm           | SOLD             | 400         | invalid case status   |
    | 106               | 206      | <h1>HTML</h1>          | <script>alert("hack")</script> | https://animals.com/dog.jpg | 306 | <b>bold</b> | available | 400 | HTML injection attempt |
    | 3.14              | 1.23     | floating_cat           | floating_name          | https://animals.com/dog.jpg  | 5.67     | floating_tag   | available        | 400         | floating-point values |
    | 108               | 208      | friendly               | buddy                  | https://animals.com/dog.jpg  | 308      | friendly       | AvAiLaBlE        | 400         | mixed-case status     |

