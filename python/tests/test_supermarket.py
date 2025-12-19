import unittest
from datetime import date

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from loyalty_program import LoyaltyAccount


class SupermarketTest(unittest.TestCase):
    def test_empty_cart(self):
        catalog = FakeCatalog()
        teller = Teller(catalog)

        cart = ShoppingCart()

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 0.0, places=2)
        self.assertEqual([], receipt.discounts)
        self.assertEqual([], receipt.items)

    def test_ten_percent_discount_negative(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        apples = Product("apples", ProductUnit.KILO)
        catalog.add_product(apples, 1.99)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

        cart = ShoppingCart()
        cart.add_item_quantity(apples, 2.5)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 4.975, places=2)
        self.assertEqual([], receipt.discounts)
        self.assertEqual(1, len(receipt.items))
        receipt_item = receipt.items[0]
        self.assertEqual(apples, receipt_item.product)
        self.assertEqual(1.99, receipt_item.price)
        self.assertAlmostEqual(receipt_item.total_price, 2.5 * 1.99, places=2)
        self.assertEqual(2.5, receipt_item.quantity)

    def test_ten_percent_discount_positive(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 1)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 0.891, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_three_for_two_less_items(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 2)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 1.98, places=2)
        self.assertEqual([], receipt.discounts)
        self.assertEqual(1, len(receipt.items))

    def test_three_for_two_discount_positive(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        teller = Teller(catalog)
        teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, toothbrush, 0
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 3)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 1.98, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_three_for_two_two_sets(self):
        catalog = FakeCatalog()
        toothbrush = Product("toothbrush", ProductUnit.EACH)
        catalog.add_product(toothbrush, 0.99)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 0)

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 6)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 3.96, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_two_for_amount_less_items(self):
        catalog = FakeCatalog()
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_special_offer(
            SpecialOfferType.TWO_FOR_AMOUNT, toothpaste, 3.00
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothpaste, 1)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 1.79, places=2)
        self.assertEqual([], receipt.discounts)
        self.assertEqual(1, len(receipt.items))

    def test_two_for_amount_discount_positive(self):
        catalog = FakeCatalog()
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_special_offer(
            SpecialOfferType.TWO_FOR_AMOUNT, toothpaste, 3.00
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothpaste, 2)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 3.00, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_five_for_amount_less_items(self):
        catalog = FakeCatalog()
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

        cart = ShoppingCart()
        cart.add_item_quantity(toothpaste, 4)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 4 * 1.79, places=2)
        self.assertEqual([], receipt.discounts)
        self.assertEqual(1, len(receipt.items))

    def test_five_for_amount_positive(self):
        catalog = FakeCatalog()
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

        cart = ShoppingCart()
        cart.add_item_quantity(toothpaste, 5)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 7.49, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_five_for_amount_with_remainder(self):
        catalog = FakeCatalog()
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)

        cart = ShoppingCart()
        cart.add_item_quantity(toothpaste, 7)

        receipt = teller.checkout_cart(cart)

        expected_total = 7.49 + 2 * 1.79
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_multiple_products_no_discounts(self):
        catalog = FakeCatalog()
        apples = Product("apples", ProductUnit.KILO)
        rice = Product("rice", ProductUnit.EACH)

        catalog.add_product(apples, 1.99)
        catalog.add_product(rice, 2.49)

        teller = Teller(catalog)

        cart = ShoppingCart()
        cart.add_item_quantity(apples, 1.0)
        cart.add_item_quantity(rice, 2)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 1.99 + 4.98, places=2)
        self.assertEqual([], receipt.discounts)

    def test_discount_applied_only_to_eligible_product(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        apples = Product("apples", ProductUnit.KILO)

        catalog.add_product(toothbrush, 0.99)
        catalog.add_product(apples, 1.99)

        teller = Teller(catalog)
        teller.add_special_offer(
            SpecialOfferType.THREE_FOR_TWO, toothbrush, 0
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 3)
        cart.add_item_quantity(apples, 1.0)

        receipt = teller.checkout_cart(cart)

        expected_total = 1.98 + 1.99
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(1, len(receipt.discounts))
        self.assertEqual(2, len(receipt.items))

# --------------------
# Bundle discounts
# --------------------

    def test_bundle_discount_applied_for_complete_bundle(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)

        catalog.add_product(toothbrush, 0.99)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)

        teller.add_bundle(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 1)
        cart.add_item_quantity(toothpaste, 1)

        receipt = teller.checkout_cart(cart)

        expected_total = (0.99 + 1.79) * 0.9
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_bundle_not_applied_when_bundle_incomplete(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)

        catalog.add_product(toothbrush, 0.99)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_bundle(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 1)

        receipt = teller.checkout_cart(cart)

        self.assertAlmostEqual(receipt.total_price(), 0.99, places=2)
        self.assertEqual([], receipt.discounts)

    def test_bundle_applied_only_for_complete_sets(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)

        catalog.add_product(toothbrush, 0.99)
        catalog.add_product(toothpaste, 1.79)

        teller = Teller(catalog)
        teller.add_bundle(
            products=[toothbrush, toothpaste],
            discount_percentage=10
        )

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 2)
        cart.add_item_quantity(toothpaste, 1)

        receipt = teller.checkout_cart(cart)

        bundle_price = 0.99 + 1.79
        expected_total = (bundle_price * 0.9) + 0.99

        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_two_different_bundles_applied(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        apples = Product("apples", ProductUnit.KILO)

        catalog.add_product(toothbrush, 0.99)
        catalog.add_product(toothpaste, 1.79)
        catalog.add_product(apples, 2.00)

        teller = Teller(catalog)
        teller.add_bundle([toothbrush, toothpaste], 10)
        teller.add_bundle([apples], 10)

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 1)
        cart.add_item_quantity(toothpaste, 1)
        cart.add_item_quantity(apples, 1)

        receipt = teller.checkout_cart(cart)

        expected_total = (0.99 + 1.79) * 0.9 + 2.00 * 0.9
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(2, len(receipt.discounts))

    def test_product_cannot_be_used_in_two_bundles(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)
        apples = Product("apples", ProductUnit.EACH)

        catalog.add_product(toothbrush, 1.00)
        catalog.add_product(toothpaste, 2.00)
        catalog.add_product(apples, 3.00)

        teller = Teller(catalog)
        teller.add_bundle([toothbrush, toothpaste], 10)
        teller.add_bundle([toothbrush, apples], 10)

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 1)
        cart.add_item_quantity(toothpaste, 1)
        cart.add_item_quantity(apples, 1)

        receipt = teller.checkout_cart(cart)

        expected_total = (1.00 + 2.00) * 0.9 + 3.00
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(1, len(receipt.discounts))

    def test_bundle_excludes_percentage_discount_for_same_product(self):
        catalog = FakeCatalog()

        toothbrush = Product("toothbrush", ProductUnit.EACH)
        toothpaste = Product("toothpaste", ProductUnit.EACH)

        catalog.add_product(toothbrush, 1.00)
        catalog.add_product(toothpaste, 2.00)

        teller = Teller(catalog)
        teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10)
        teller.add_bundle([toothbrush, toothpaste], 10)

        cart = ShoppingCart()
        cart.add_item_quantity(toothbrush, 1)
        cart.add_item_quantity(toothpaste, 1)

        receipt = teller.checkout_cart(cart)

        expected_total = (1.00 + 2.00) * 0.9
        self.assertAlmostEqual(receipt.total_price(), expected_total, places=2)
        self.assertEqual(1, len(receipt.discounts))

# --------------------
# Coupon-based discounts
# --------------------

    def test_coupon_not_applied_outside_valid_date(self):
        catalog = FakeCatalog()
        milk = Product("milk", ProductUnit.EACH)
        catalog.add_product(milk, 2.00)

        teller = Teller(catalog)
        teller.add_coupon(
            product=milk,
            buy_quantity=2,
            discounted_quantity=2,
            discount_percentage=50,
            date_start=date(2024, 1, 1),
            date_end=date(2024, 1, 2),
        )

        cart = ShoppingCart()
        cart.add_item_quantity(milk, 2)

        receipt = teller.checkout_cart(cart, today=date(2024, 1, 10))

        self.assertAlmostEqual(receipt.total_price(), 4.00)
        self.assertEqual([], receipt.discounts)

    def test_coupon_not_applied_when_quantity_too_low(self):
        catalog = FakeCatalog()
        juice = Product("juice", ProductUnit.EACH)
        catalog.add_product(juice, 3.00)

        teller = Teller(catalog)
        teller.add_coupon(
            product=juice,
            buy_quantity=2,
            discounted_quantity=2,
            discount_percentage=50,
            date_start=date(2024, 1, 1),
            date_end=date(2024, 12, 31),
        )

        cart = ShoppingCart()
        cart.add_item_quantity(juice, 1)

        receipt = teller.checkout_cart(cart, today=date(2024, 6, 1))

        self.assertAlmostEqual(receipt.total_price(), 3.00)
        self.assertEqual([], receipt.discounts)

    def test_coupon_applied_correctly(self):
        catalog = FakeCatalog()
        juice = Product("juice", ProductUnit.EACH)
        catalog.add_product(juice, 3.00)

        teller = Teller(catalog)
        teller.add_coupon(
            product=juice,
            buy_quantity=2,
            discounted_quantity=2,
            discount_percentage=50,
            date_start=date(2024, 12, 24),
            date_end=date(2024, 12, 31),
        )

        cart = ShoppingCart()
        cart.add_item_quantity(juice, 2)

        receipt = teller.checkout_cart(cart, today=date(2024, 12, 25))

        expected_total = 3.00 + (3.00 * 0.5)
        self.assertAlmostEqual(receipt.total_price(), expected_total)
        self.assertEqual(1, len(receipt.discounts))

    def test_coupon_used_only_once(self):
        catalog = FakeCatalog()
        juice = Product("juice", ProductUnit.EACH)
        catalog.add_product(juice, 3.00)

        teller = Teller(catalog)
        coupon = teller.add_coupon(
            product=juice,
            buy_quantity=2,
            discounted_quantity=2,
            discount_percentage=50,
            date_start=date(2025, 12, 1),
            date_end=date(2025, 12, 31),
        )

        cart = ShoppingCart()
        cart.add_item_quantity(juice, 2)

        receipt1 = teller.checkout_cart(cart, today=date(2025, 12, 24))
        receipt2 = teller.checkout_cart(cart, today=date(2025, 12, 24))

        self.assertEqual(1, len(receipt1.discounts))
        self.assertEqual([], receipt2.discounts)

# --------------------
# Loyalty program
# --------------------

    def test_loyalty_points_earned_after_purchase(self):
        catalog = FakeCatalog()
        cheese = Product("cheese", ProductUnit.EACH)
        catalog.add_product(cheese, 120.00)

        teller = Teller(catalog)
        loyalty_account = LoyaltyAccount()

        cart = ShoppingCart()
        cart.add_item_quantity(cheese, 1)

        receipt = teller.checkout_cart(cart, loyalty_account=loyalty_account)

        self.assertEqual(2, loyalty_account.points)

    def test_loyalty_points_used_as_payment(self):
        catalog = FakeCatalog()
        milk = Product("milk", ProductUnit.EACH)
        catalog.add_product(milk, 10.00)

        teller = Teller(catalog)
        loyalty_account = LoyaltyAccount()
        loyalty_account.points = 5

        cart = ShoppingCart()
        cart.add_item_quantity(milk, 1)

        receipt = teller.checkout_cart(cart, loyalty_account=loyalty_account)

        self.assertAlmostEqual(receipt.total_price(), 5.00)
        self.assertEqual(0, loyalty_account.points)

    def test_partial_payment_with_loyalty_points(self):
        catalog = FakeCatalog()
        bread = Product("bread", ProductUnit.EACH)
        catalog.add_product(bread, 8.00)

        teller = Teller(catalog)
        loyalty_account = LoyaltyAccount()
        loyalty_account.points = 3

        cart = ShoppingCart()
        cart.add_item_quantity(bread, 1)

        receipt = teller.checkout_cart(cart, loyalty_account=loyalty_account)

        self.assertAlmostEqual(receipt.total_price(), 5.00)
        self.assertEqual(0, loyalty_account.points)

