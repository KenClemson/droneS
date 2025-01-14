

Feature: Creating orders should show correct order amounts
  A User can purchase items from the store
  In order to purchase items the user can select items
  and add them to the cart.
  Users can then checkout the cart and the order amounts should be correct

  Scenario Outline: Check order amounts for each test customer
    Given I am on the login page
    When I enter <username> and <password>
    And I click the login button
    Given I am on the products page
    When I add "Sauce Labs Backpack" to the cart
    When I add "Sauce Labs Bike Light" to the cart
    When I add "Sauce Labs Fleece Jacket" to the cart
    When I add "Sauce Labs Bolt T-Shirt" to the cart
    When I add "Sauce Labs Onesie" to the cart
    When I add "Test.allTheThings() T-Shirt (Red)" to the cart
    When I open the shopping cart

    Then The prices in the cart match the product prices
    When I click on the cart checkout button
    Then I should be directed to the checkout step 1 page

    #Negative testing to test the correct errors
    When I click continue
    Then I should see the error message Error: First Name is required
    When I fill in First Name with John
    When I leave Last Name empty
    And I fill in Zip/Postal Code with 12345
    When I click continue
    Then I should see the error message Error: Last Name is required

    When I fill the order form with TestFirstName TestLastName and 1234
    When I click continue
    Then I should be directed to the checkout step 2 page

    Then the order amount should be correct on the overview page


    Examples:
      | username | password |
      |   standard_user | secret_sauce |
      |   problem_user  | secret_sauce |
      |   performance_glitch_user | secret_sauce |
      |   visual_user | secret_sauce |
      |   error_user  | secret_sauce |


