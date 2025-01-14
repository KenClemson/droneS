Feature: User Login
  In order to access the secure area of the website,
  Users should be able to log in with valid and invalid credentials.

  Scenario Outline: Attempt login with correct and not accepted characters
    Given I am on the login page
    When I enter <username> and <password>
    And I click the login button
    Then I should see <expected_outcome>

    Examples:
      | username             | password               | expected_outcome                |
      | standard_user         | secret_sauce           | successful login                |
#      | locked_out_user       | secret_sauce           | locked out error                |
#      | "    "                | secret_sauce           | missing username error          |
#      | standard_user         | "    "                 | missing password error          |
#      | ""                    | ""                     | missing username/password error |
#      | invalid_user          | wrong_pass             | login failed                    |
#      | "<script>alert(1);</script>" | secret_sauce   | login failed (invalid input)    |
#      | admin' OR 1=1; --     | secret_sauce           | login failed (injection attempt)|
#      | 😀😁😂                 | secret_sauce           | login failed (invalid characters)|
#      | standard_user         | "P@$$w0rd!"            | login failed (wrong password)   |
#      | performance_glitch_user | secret_sauce         | slow login but successful       |
#      | standard_user         | Secret_Sauce           | login failed (case-sensitive)   |
#      | verylonguser1234567890123456789012345678901234567890 | secret_sauce | login failed (username too long) |
#      | standard_user         | supersecurepasswordthatkeepsgoingforever | login failed (password too long) |



