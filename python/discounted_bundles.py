from model_objects import Discount


class BundleDiscountApplier:
    def apply(self, receipt, bundles, product_quantities, catalog):
        remaining_quantities = dict(product_quantities)
        products_used_in_bundles = set()

        for bundle in bundles:
            bundle_quantities = [
                remaining_quantities.get(product, 0)
                for product in bundle.products
            ]

            complete_sets = min(bundle_quantities)
            if complete_sets <= 0:
                continue

            bundle_price = sum(
                catalog.unit_price(product)
                for product in bundle.products
            )

            discount_total = (
                bundle_price
                * complete_sets
                * bundle.discount_percentage
                / 100.0
            )

            receipt.add_discount(
                Discount(
                    None,
                    f"Bundle {bundle.discount_percentage}% off",
                    -discount_total
                )
            )

            for product in bundle.products:
                remaining_quantities[product] -= complete_sets
                products_used_in_bundles.add(product)

        self._remove_percentage_discounts(receipt, products_used_in_bundles)

    def _remove_percentage_discounts(self, receipt, products_used_in_bundles):
        receipt._discounts = [
            discount for discount in receipt.discounts
            if not (
                discount.product in products_used_in_bundles
                and discount.description.endswith("% off")
            )
        ]
