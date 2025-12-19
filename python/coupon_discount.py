from model_objects import Discount


class CouponApplier:
    def apply(self, receipt, coupons, product_quantities, catalog, today):
        for coupon in coupons:
            if coupon.used:
                continue

            if not (coupon.date_start <= today <= coupon.date_end):
                continue

            quantity = product_quantities.get(coupon.product, 0)
            if quantity < coupon.buy_quantity:
                continue

            unit_price = catalog.unit_price(coupon.product)

            #discounted_items = min(coupon.discounted_quantity, quantity - coupon.buy_quantity)
            #if discounted_items == 0:
            #    continue

            discount_amount = (
                unit_price
                * (coupon.discount_percentage / 100.0)
            )

            receipt.add_discount(
                Discount(
                    coupon.product,
                    f"Coupon {coupon.discount_percentage}% off",
                    -discount_amount
                )
            )

            coupon.used = True
