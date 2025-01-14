# TEST STRATEGY

## 1.1 Project Overview
The system under test is an **E-Commerce Web Application** that allows users to perform various actions such as:

- Logging in
- Selecting clothing items
- Filtering by price and alphabetical order
- Adding and removing items from the shopping cart
- Entering shipping details
- Purchasing items

---

## 1.2 Scope of Testing

### **In-Scope Functionality**
- User Login
- Item Selection and Filtering
- Shopping Cart Management
- Shipping Details Entry
- Testing correct costings
- Purchase Flow

### **Out-of-Scope Functionality**
- Payment gateway integration
- Post-purchase email notifications

---

## 1.3 Types of Testing

- **Functional Testing**: Verify correct behavior of all critical workflows.
- **UI Testing**: Validate the layout and behavior of UI components.
- **Usability Testing**: Assess the ease of use and navigation of the application.
- **Exploratory Testing**: Perform unscripted testing to identify unexpected issues.

---

## 1.4 Test Approach (Strategy)
- **Automation Framework**: Pytest-BDD with Selenium.

### **Automation Scope**
- Automate regression tests for critical user flows.
- Gherkin syntax for BDD to improve test readability and collaboration.

### **Manual Testing Scope**
- Perform manual exploratory and usability testing to capture issues not covered by automated tests.

### **Bug Tracking Tool**
- **JIRA** for tracking defects and reporting.

---

# 2. TEST PLANS

## 2.1 Test Environment and Tools
- **Environment**: Staging Environment
- **Browsers**: Chrome, Firefox, Edge (latest versions)
- **Tools**: Pytest BDD, Selenium WebDriver, JIRA

---

## 2.2 Test Data
- **User Credentials**: Valid and invalid test accounts.
- **Product Data**: Sample clothing items with various prices and categories. Developers or testers can input data.
- **Shipping Data**: Mock user details for address entry.

---

## 2.3 Risks and Mitigation

| **Risk**                | **Impact** | **Mitigation**                                                    |
|-------------------------|------------|-------------------------------------------------------------------|
| Environment downtime     | High       | Coordinate with DevOps team for early setup.                      |
| Unstable test data       | Medium     | Generate and validate test data before testing.                   |
| Limited testing time (3 weeks) | High | Prioritize critical test cases and automate key flows.            |
| Flaky automated tests    | Medium     | Implement reliable waits, retries, and assertions.                |

---

## 2.4 Entry and Exit Criteria

### **Entry Criteria**
- All necessary features have been implemented.
- Test data and staging environment are ready.

### **Exit Criteria**
- All critical defects have been fixed or deferred with approval.
- Regression tests for key workflows have passed.

---

# DECISIONS AND REASONS

### **Pytest BDD + Selenium for Automation**
- **Reason**: Pytest BDD improves collaboration with stakeholders, and Selenium provides comprehensive UI interaction capabilities.
- Manual testers can easily write Gherkin tests, and automation testers can automate them.

### **Manual Exploratory Testing**
- **Reason**: Identifies UX and usability issues that cannot be easily detected by automated tests.

### **Focus on Critical Flows First**
- **Reason**: To ensure the most important user journeys (e.g., login, add to cart, checkout) are stable within the short sprint timeframe.
- Automate the most important user journeys first.

---

# Test Cases

## **Navigation and Menu Tests**

| **Test Case**             | **Steps**                                | **Expected Result**                                                |
|---------------------------|------------------------------------------|--------------------------------------------------------------------|
| Open hamburger menu        | Click the hamburger button               | Menu opens with options "All Items", "About", "Logout", "Reset App". |
| Logout from menu           | Open menu/Click "Logout"                 | User is logged out and redirected to the login page.               |
| Reset App State            | Add items/Open menu/Click Reset          | Shopping cart is emptied; filters reset to default.                |

---

## **Product Inventory List Tests**

| **Test Case**             | **Steps**                                | **Expected Result**                                                |
|---------------------------|------------------------------------------|--------------------------------------------------------------------|
| Add product to cart        | Click "Add to cart" for a product        | "Add to cart" button changes to "Remove".                         |
| Verify sorting "Price (low to high)" | Select "Price (low to high)" in sort options | Products are sorted in ascending price. |
| Invalid product addition   | Log in with "problem_user" and add items | Error: Products cannot be added or removed.                       |

---

## **Edge Cases**

| **Test Case**              | **Steps**                                | **Expected Result**                                                |
|----------------------------|------------------------------------------|--------------------------------------------------------------------|
| Add same product multiple times | Add the same product repeatedly to the cart | No duplicates appear in the cart.                                |
| Reset app after logout      | Add items → Logout → Log in → Reset app | Cart is empty after re-login.                                     |
