# Bug Report

**Summary:**  
Multiple issues have been identified across various user roles in the system, indicating inconsistencies in functionality, performance, and UI/UX components.

## Overview of Findings

### Login Page Issues  
- Error messages are cut off within the bounds of the red box.

### Filter Button Issues  
- The down-facing triangle on filter buttons is unclickable for standard users.  
- Filters cannot be set for problem users.

### Cart and Checkout Inconsistencies  
- Red cart count inconsistencies after reset.  
- Ability to complete an empty order.  
- Missing checkout button in the cart for visual users.

### UI/UX Issues  
- Misaligned footer, hamburger menu, and checkout button.  
- Dog image incorrectly displayed instead of the backpack.

### Performance Issues  
- Severe performance lags when using `performance_glitch_user`.

### Item and Cart Management Problems  
- "Add to Cart" buttons are non-functional for specific items for problem users.  
- Items cannot be removed after being added for both error users and problem users.

### Incorrect Functionality  
- Clicking on the "About" link causes a 404 error.  
- Clicking "All Items" in the hamburger menu changes item prices.

### Form Field Issue  
- Entering a last name adds characters to the first name field.

## Impact

- **User Experience:** High impact on user trust due to multiple UI/UX inconsistencies and incorrect image displays.  
- **Functional Integrity:** Core functionalities such as cart management, filtering, and checkout are affected.  
- **Performance:** Slower load times and responsiveness hinder usability for certain roles.

## Recommendations

1. **Performance and Cart-Related Issues:**  
   - Prioritize fixing performance lags and cart-related issues to maintain core functionality.
   
2. **Regression Testing:**  
   - Implement thorough regression tests for UI elements and form validation.
   
3. **Backend and API Review:**  
   - Review API and backend connections for handling item additions and resets.
   
4. **404 Error Resolution:**  
   - Address "About" page 404 errors by ensuring proper routing.

## Next Steps

- Assign individual bug fixes to relevant teams based on categories such as UI/UX, performance, and backend.  
- Monitor resolutions and conduct system-wide testing before deployment.

This report provides a high-level summary of all identified issues to assist in tracking progress and prioritization.



## JIRA BUG TICKETS TO BE ASSIGNED IN SPRINT

## DRNSHLD 10001: Login Page Error Message Cutoff

**Summary:** The error message text is truncated inside the bounds of the red box.

**Severity:** MEDIUM

**Steps to Reproduce:**  
1. Navigate to the login page.  
2. Trigger an error (e.g., enter incorrect credentials).  

**Expected Result:** The error message should be fully visible inside the red box.  
**Actual Result:** The text is cut off.

---

## DRNSHLD 10002: Filter Button Click Issue

**Summary:** The down-facing triangle on filter buttons cannot be clicked.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a standard user.  
2. Attempt to click the down-facing triangle on the filter button.  

**Expected Result:** The filter dropdown should expand.  
**Actual Result:** The filter button does not respond to clicks.

---

## DRNSHLD 10003: Red Cart Number Disappears on Reset

**Summary:** Reset app state causes the red number to disappear from the trolley but not from the cart.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a standard user.  
2. Add items to the cart.  
3. Navigate to the cart page.  
4. Click on Hamburger Menu > Reset App.  

**Expected Result:** Both the cart and trolley indicators should be reset.  
**Actual Result:** The trolley number disappears, but the cart number remains.

---

## DRNSHLD 10004: Empty Order Completion

**Summary:** It is possible to complete an order without adding any items.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a standard user.  
2. Navigate to checkout without adding items.  
3. Complete the checkout process.  

**Expected Result:** An error should prevent order completion without items.  
**Actual Result:** The system allows the order to be completed.

---

## DRNSHLD 10005: Reset App Does Not Reset Filters

**Summary:** Resetting the app state does not revert the filters to default values.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a standard user.  
2. Apply any filter.  
3. Click on Hamburger Menu > Reset App.  

**Expected Result:** All filters should be reset to default.  
**Actual Result:** The filters remain unchanged.

---

## DRNSHLD 10006: Incorrect Images for Problem User

**Summary:** Incorrect images are displayed when logged in as a problem user.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a problem user.  
2. Browse through the item list.  

**Expected Result:** Correct images should be displayed.  
**Actual Result:** Incorrect images are shown.

---

## DRNSHLD 10007: Unable to Set Filters as Problem User

**Summary:** Filters cannot be set when logged in as a problem user.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a problem user.  
2. Attempt to set any filter.  

**Expected Result:** Filters should be applicable.  
**Actual Result:** Filter settings do not work.

---

## DRNSHLD 10008: Add to Cart Button Non-Functional

**Summary:** Add to cart buttons 3, 4, and 6 do not respond when clicked for the problem user.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a problem user.  
2. Attempt to add items 3, 4, and 6 to the cart.  

**Expected Result:** Items should be added to the cart.  
**Actual Result:** Clicking the buttons has no effect.

---

## DRNSHLD 10009: Cannot Remove Items from Cart

**Summary:** Items added to the cart cannot be removed for the problem user.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a problem user.  
2. Add any removable item.  
3. Attempt to remove the item.  

**Expected Result:** Items should be removable.  
**Actual Result:** Items cannot be removed.

---

## DRNSHLD 10010: 404 Error on About Page

**Summary:** Clicking on Hamburger Menu > About causes a 404 error.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as a problem user.  
2. Click Hamburger Menu > About.  

**Expected Result:** The About page should load.  
**Actual Result:** A 404 error is displayed.

---

## DRNSHLD 10011: Last Name Field Alters First Name Field

**Summary:** Entering a last name adds a single character to the first name field.

**Severity:** VERY HIGH

**Steps to Reproduce:**  
1. Navigate to the Checkout > Your Information page.  
2. Enter text in the Last Name field.  

**Expected Result:** No changes to the first name field.  
**Actual Result:** A single character is added to the first name field.

---

## DRNSHLD 10012: Performance Issue with Performance Glitch User

**Summary:** Severe performance issues occur when logging in as the performance_glitch_user.

**Severity:** VERY HIGH

**Steps to Reproduce:**  
1. Log in as performance_glitch_user.  

**Expected Result:** Smooth navigation and interactions.  
**Actual Result:** Slow performance and noticeable lags.

---

## DRNSHLD 10013: Item Removal Failure for Error User

**Summary:** Items cannot be removed after being added to the cart when logged in as error user.

**Severity:** VERY HIGH

**Steps to Reproduce:**  
1. Log in as error user.  
2. Add an item to the cart.  
3. Attempt to remove the item.  

**Expected Result:** Items should be removable.  
**Actual Result:** Items cannot be removed.

---

## DRNSHLD 10014: Incorrect Image Displayed for Visual User

**Summary:** The first item displays a dog image instead of a backpack.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as visual user.  
2. View the first item.  

**Expected Result:** The image should display a backpack.  
**Actual Result:** The image shows a dog.

---

## DRNSHLD 10015: Cart Price Mismatch for Visual User

**Summary:** Prices in the cart do not match the displayed item prices.

**Severity:** VERY HIGH

**Steps to Reproduce:**  
1. Log in as visual user.  
2. Add items to the cart.  
3. Compare prices between the item list and cart.  

**Expected Result:** Prices should match.  
**Actual Result:** Prices are inconsistent.

---

## DRNSHLD 10016: Misaligned Checkout Button and Trolley Icon

**Summary:** The checkout button and trolley icon are out of place.

**Severity:** MEDIUM

**Steps to Reproduce:**  
1. Log in as visual user.  
2. Observe the position of the checkout button and trolley icon.  

**Expected Result:** Elements should be correctly aligned.  
**Actual Result:** Elements are misaligned.

---

## DRNSHLD 10017: Hamburger Menu Angle Issue

**Summary:** The hamburger menu appears at a slight angle.

**Severity:** MEDIUM

**Steps to Reproduce:**  
1. Log in as visual user.  
2. Observe the hamburger menu.  

**Expected Result:** The menu should be straight.  
**Actual Result:** The menu is angled.

---

## DRNSHLD 10018: Prices Change When Selecting All Items

**Summary:** Clicking Hamburger > All Items changes the prices of all items.

**Severity:** VERY HIGH

**Steps to Reproduce:**  
1. Log in as visual user.  
2. Click Hamburger Menu > All Items.  

**Expected Result:** Prices should remain unchanged.  
**Actual Result:** Prices change unexpectedly.

---

## DRNSHLD 10019: Footer Misalignment

**Summary:** The footer is out of place on the page.

**Severity:** MEDIUM

**Steps to Reproduce:**  
1. Log in as visual user.  
2. Scroll to the footer.  

**Expected Result:** Footer should be properly aligned.  
**Actual Result:** Footer is misaligned.

---

## DRNSHLD 10020: Add to Cart Button Misplacement

**Summary:** The "Add to Cart" button for the 6th item is out of place.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as visual user.  
2. View the 6th item.  

**Expected Result:** Button should be properly positioned.  
**Actual Result:** Button is misplaced.

---

## DRNSHLD 10021: Missing Checkout Button

**Summary:** The checkout button is missing from the cart.

**Severity:** HIGH

**Steps to Reproduce:**  
1. Log in as visual user.  
2. Add items to the cart.  
3. Navigate to the cart.  

**Expected Result:** Checkout button should be present.  
**Actual Result:** No checkout button is visible.
