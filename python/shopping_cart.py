from model_objects import ProductQuantity, SpecialOfferType, Discount
from discounted_bundles import BundleDiscountApplier
from coupon_discount import CouponApplier


class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}
        self._discount_strategies = {
            SpecialOfferType.THREE_FOR_TWO: self._three_for_two,
            SpecialOfferType.TWO_FOR_AMOUNT: self._two_for_amount,
            SpecialOfferType.FIVE_FOR_AMOUNT: self._five_for_amount,
            SpecialOfferType.TEN_PERCENT_DISCOUNT: self._ten_percent_discount,
        }
        self._bundle_applier = BundleDiscountApplier()
        self._coupon_applier = CouponApplier()

    @property
    def items(self):
        return self._items

    @property
    def product_quantities(self):
        return self._product_quantities

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] = self._product_quantities[product] + quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for product, quantity in self._product_quantities.items():
            if product in offers:
                offer = offers[product]
                unit_price = catalog.unit_price(product)

                discount = self.calculate_discount(offer, product, quantity, unit_price)

                if discount:
                    receipt.add_discount(discount)

    def handle_bundles(self, receipt, bundles, catalog):
        self._bundle_applier.apply(receipt, bundles, self._product_quantities, catalog)

    def handle_coupons(self, receipt, coupons, catalog, today):
        self._coupon_applier.apply(receipt, coupons, self._product_quantities, catalog, today)

    def calculate_discount(self, offer, product, quantity, unit_price):
        quantity_as_int = int(quantity)
        normal_total = quantity_as_int * unit_price

        strategy = self._discount_strategies.get(offer.offer_type)
        if not strategy:
            return None

        discounted_total = strategy(offer, quantity_as_int, unit_price)
        discount_value = normal_total - discounted_total

        if discount_value > 0:
            return Discount(product, self._discount_description(offer), -discount_value)

        return None

    def _three_for_two(self, offer, quantity, unit_price):
        if quantity < 3:
            return quantity * unit_price
        sets = quantity // 3
        rest = quantity % 3
        return (sets * 2 + rest) * unit_price

    def _two_for_amount(self, offer, quantity, unit_price):
        if quantity < 2:
            return quantity * unit_price
        sets = quantity // 2
        rest = quantity % 2
        return (sets * offer.argument) + (rest * unit_price)

    def _five_for_amount(self, offer, quantity, unit_price):
        if quantity < 5:
            return quantity * unit_price
        sets = quantity // 5
        rest = quantity % 5
        return (sets * offer.argument) + (rest * unit_price)

    def _ten_percent_discount(self, offer, quantity, unit_price):
        return quantity * unit_price * (1 - offer.argument / 100.0)

    def _discount_description(self, offer):
        if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
            return "3 for 2"
        if offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
            return f"2 for {offer.argument}"
        if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
            return f"5 for {offer.argument}"
        if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
            return f"{offer.argument}% off"
