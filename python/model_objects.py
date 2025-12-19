from enum import Enum


class Product:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit


class ProductQuantity:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


class Offer:
    def __init__(self, offer_type, product, argument):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument


class Discount:
    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount


class Bundle:
    def __init__(self, products, discount_percentage):
        self.products = products
        self.discount_percentage = discount_percentage


class Coupon:
    def __init__(self, product, buy_quantity, discounted_quantity, discount_percentage, date_start, date_end):
        self.product = product
        self.buy_quantity = buy_quantity
        self.discounted_quantity = discounted_quantity
        self.discount_percentage = discount_percentage
        self.date_start = date_start
        self.date_end = date_end
        self.used = False
