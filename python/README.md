# Supermarket Receipt in [Python](https://www.python.org/)

## Setup

* Have Python installed
* Clone the repository
* On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory
* On the command line, install requirements, e.g. on the`python -m pip install -r requirements.txt`

## Running Tests

On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory and run

```
python -m unittest
```

## Optional: Running [TextTest](https://www.texttest.org/) Tests

Install TextTest according to the [instructions](https://www.texttest.org/index.html#getting-started-with-texttest) (platform specific).

On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory and run

```
texttest -a sr -d .
```

## Testing

I started by extending the test suite to cover all existing pricing rules and edge cases. The tests verify both positive and negative scenarios, such as discounts being applied only when conditions are met and not applied otherwise.

The test suite covers:

* Percentage discounts, fixed-amount offers, and multi-buy promotions
* Scenarios where discounts should not be applied
* Multiple products in the cart
* Empty cart behavior

After refactoring, I added dedicated test sections for each new feature (bundles, coupons, and loyalty program)

## Identified code smells and refactorings

One of the main issues in the original code was the Long Method smell. The checkout and discount logic contained deeply nested conditional statements and multiple responsibilities in a single place. This made the code difficult to read, test, and extend.

To address this, I extracted smaller, well-named methods and introduced dedicated classes responsible for applying specific discount rules. In particular:

* Bundle-related logic was moved to a separate BundleDiscountApplier class.
* Coupon-related logic was moved to a separate CouponApplier class.
* Discount calculation logic in ShoppingCart was refactored using a strategy-like mapping instead of large conditional blocks.

I also noticed some kind of duplication, where there were different methods of calculating promotions. I tried to standardise them.

Another issue was Feature Envy, where certain methods depended heavily on data from other objects. This was mitigated by moving discount application logic closer to the data it operates on and by passing only the necessary inputs to each component.

---

## Implemented features

### Standard special offers

All original special offers are supported:
- Three for two
- Two for a fixed amount
- Five for a fixed amount
- Percentage discounts

Each offer:
- Applies only when eligibility conditions are met
- Is listed explicitly on the receipt
- Does not affect unrelated products

### Discounted bundles

Characteristics:
- A bundle consists of one or more products
- A percentage discount is applied only to complete bundle sets
- Incomplete bundles are not discounted
- A product cannot be used in more than one bundle
- Bundle discounts take precedence over percentage discounts for the same product

The bundle logic is encapsulated in a dedicated class and covered by tests.

### Coupon-based discounts

Characteristics:
- Coupons apply to a specific product
- They are valid only within a given date range
- A minimum quantity must be purchased
- Only a limited number of items can be discounted
- Each coupon can be used only once

Coupon validation and application logic is isolated in the `CouponApplier` class.

### Loyalty program

Characteristics:
- Customers earn 1 point for every 50 currency units spent
- 1 point can be redeemed as 1 currency unit
- Points can be used as full or partial payment
- Remaining amount (after redemption) still earns new points

The loyalty program is optional and does not affect checkout if no loyalty account is provided.

---
