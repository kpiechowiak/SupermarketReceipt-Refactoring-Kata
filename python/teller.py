from model_objects import Offer, Bundle, Coupon, Discount
from receipt import Receipt
from datetime import date


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}
        self.bundles = []
        self.coupons = []

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def add_bundle(self, products, discount_percentage):
        self.bundles.append(Bundle(products, discount_percentage))

    def add_coupon(self, **kwargs):
        coupon = Coupon(**kwargs)
        self.coupons.append(coupon)
        return coupon

    def checkout_cart(self, cart, today=None, loyalty_account=None):
        if today is None:
            today = date.today()

        receipt = Receipt()
        self._add_cart_items_to_receipt(receipt, cart)
        cart.handle_offers(receipt, self.offers, self.catalog)
        cart.handle_bundles(receipt, self.bundles, self.catalog)
        cart.handle_coupons(receipt, self.coupons, self.catalog, today)

        total = receipt.total_price()

        if loyalty_account:
            redeemed = loyalty_account.redeem(total)
            if redeemed > 0:
                receipt.add_discount(
                    Discount(
                        None,
                        "Loyalty points",
                        -redeemed
                    )
                )

            loyalty_account.add_points(total - redeemed)

        return receipt

    def _add_cart_items_to_receipt(self, receipt, the_cart):
        for pq in the_cart.items:
            product = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(product)
            price = quantity * unit_price
            receipt.add_product(product, quantity, unit_price, price)
