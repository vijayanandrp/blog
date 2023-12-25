import datetime

store_name = """

:'######::'##::::'##::'#######::'########::'##:::'##::::'###::::'########::'########:
'##... ##: ##:::: ##:'##.... ##: ##.... ##: ##::'##::::'## ##::: ##.... ##:... ##..::
 ##:::..:: ##:::: ##: ##:::: ##: ##:::: ##: ##:'##::::'##:. ##:: ##:::: ##:::: ##::::
. ######:: #########: ##:::: ##: ########:: #####::::'##:::. ##: ########::::: ##::::
:..... ##: ##.... ##: ##:::: ##: ##.....::: ##. ##::: #########: ##.. ##:::::: ##::::
'##::: ##: ##:::: ##: ##:::: ##: ##:::::::: ##:. ##:: ##.... ##: ##::. ##::::: ##::::
. ######:: ##:::: ##:. #######:: ##:::::::: ##::. ##: ##:::: ##: ##:::. ##:::: ##::::
:......:::..:::::..:::.......:::..:::::::::..::::..::..:::::..::..:::::..:::::..:::::
                                                                                                                                                                                                 
"""


def currency(value, country="en_GB"):
    if country == "en_GB":
        return f"£{value:4.2f}" if value >= 1 else f"{int(value*100):<2d}p"
    elif country == "en_US":
        return f"${value:4.2f}" if value >= 1 else f"{int(value*100):<2d}c"


class NotEnoughCartItem(Exception):
    def __init__(self):
        super().__init__("Not enough items in the cart")


class NotEnoughInventoryItem(Exception):
    def __init__(self):
        super().__init__("Not enough items in the inventory")


class InvalidInput(Exception):
    pass


class Product:
    def __init__(self, product_id: int, name: str, price: float) -> None:
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self) -> str:
        return f"Product: {self.name:<12} | Price: {currency(self.price):<12}"


class InventoryItem:
    def __init__(self, product: Product) -> None:
        self.product = product
        self.count = 0

    def update_item_count(self, count: int) -> None:
        if count == 0:
            return
        if count < 0 and self.count < count:
            raise NotEnoughInventoryItem()

        self.count += count

    def __str__(self) -> str:
        return f"{self.product} | Count: {self.count:<4d}"


class Inventory:
    def __init__(self) -> None:
        self.items: dict[int, InventoryItem] = dict()

    def add_item(self, product: Product, count: int = 1) -> None:
        if count <= 0:
            raise InvalidInput("Count must be a positive integer.")

        item = self.items.setdefault(product.product_id, InventoryItem(product))
        item.update_item_count(count=count)

    def remove_item(self, product: Product, count: int = 1) -> None:
        if count <= 0:
            raise InvalidInput("Count must be a positive integer.")

        item = self.items.get(product.product_id)
        if not item or item.count < count:
            raise NotEnoughInventoryItem()

        item.update_item_count(count=-count)

    def check_stock(self, product: Product, count: int) -> bool:
        item = self.items.get(product.product_id, None)
        if not item or item.count < count:
            return False

        return True

    def __str__(self) -> str:
        result = "Inventory\n--------\n" + "\n".join(
            str(v) for v in self.items.values()
        )
        return result


class CartItem:
    def __init__(self, product: Product) -> None:
        self.product = product
        self.count = 0
        self.total_price = 0

    def update_item_count(self, count: int) -> float:
        self.count += count

        price_delta = self.product.price * count
        self.total_price += price_delta

        return price_delta

    def recalculate_total_price(self) -> None:
        """
        If the price of a product gets changed after the product is added to the cart,
        the cart should reflect it.
        """
        self.total_price = self.product.price * self.count

    def __str__(self) -> str:
        return (
            f"Product: {self.product.name:<12} | Count: {self.count:<4d} | "
            f"Total: {currency(self.total_price):<12}"
        )


class Cart:
    def __init__(self) -> None:
        self.items: dict[int, CartItem] = {}
        self.total_price = 0

    def add_item(self, product: Product, count: int = 1) -> None:
        if count <= 0:
            raise InvalidInput("Count must be a positive integer.")

        item = self.items.setdefault(product.product_id, CartItem(product))
        price_delta = item.update_item_count(count=count)
        self.total_price += price_delta

    def remove_item(self, product: Product, count: int = 1) -> None:
        if count <= 0:
            raise InvalidInput("Count must be a positive integer.")

        item = self.items.get(product.product_id)
        if not item or item.count < count:
            raise NotEnoughCartItem()

        price_delta = item.update_item_count(count=-count)
        self.total_price += price_delta

        if item.count == 0:
            del self.items[product.product_id]

    def delete_item(self, product: Product) -> None:
        item = self.items.get(product.product_id, None)
        if item:
            self.remove_item(product=product, count=item.count)

    def empty_cart(self):
        self.items.clear()
        self.total_price = 0

    def recalculate_total_prices(self) -> None:
        self.total_price = 0
        for item in self.items.values():
            item.recalculate_total_price()
            self.total_price += item.total_price

    def __str__(self) -> str:
        result = (
            f"Cart - ({datetime.datetime.now()})\n----\n"
            + "\n".join(str(item) for item in self.items.values())
            + f" \nTotal Price: {currency(self.total_price):<20s}"
        )
        return result


class BasePromotion:
    def __init__(self, name: str) -> None:
        self.name = name

    def apply_promotion(self, count: int, product_price: float) -> float:
        raise NotImplementedError()


class DiscountPromotion(BasePromotion):
    def __init__(self, name: str, discount_percentage: float) -> None:
        super().__init__(name=name)
        self.multiplier = 1 - discount_percentage / 100

    def apply_promotion(self, count: int, product_price: float) -> float:
        return count * product_price * self.multiplier


class BuyOneGetXPromotion(BasePromotion):
    def __init__(self, name: str, x: int) -> None:
        if x <= 0:
            raise InvalidInput("x must be a positive integer")
        super().__init__(name=name)
        self.x = x

    def apply_promotion(self, count: int, product_price: float) -> float:
        divider = self.x + 1
        return (count // divider + (0 if count % divider == 0 else 1)) * product_price


class ReceiptItem:
    def __init__(
        self,
        product_name: str,
        price: float,
        count: int,
        original_total: float,
        final_total: float,
    ) -> None:
        self.product_name = product_name
        self.price = price
        self.count = count
        self.original_total = original_total
        self.final_total = final_total

    def __str__(self) -> str:
        return (
            f"{self.product_name:<12}: {currency(self.price):>5} * {self.count}| "
            f" Original: {currency(self.original_total):<12s}"
            f" => Final: {currency(self.final_total):<12s}"
        )


class Receipt:
    def __init__(self) -> None:
        self.items: list[ReceiptItem] = []
        self.original_total = 0
        self.final_total = 0

    def add_item(self, item: ReceiptItem):
        self.items.append(item)

    def __str__(self) -> str:
        result = (
            "Receipt\n-------\n"
            + "\n".join(str(item) for item in self.items)
            + f"\nOriginal Total: {currency(self.original_total)}"
            + f" => Final Total: {currency(self.final_total)}\n"
        )
        return result


class CheckoutManager:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.promotions: dict[int, BasePromotion] = dict()

    def add_promo(self, product_id: int, promo: BasePromotion) -> None:
        # Product does not need to exist in the inventory since the user may add the promo first.
        # Latest promo overrides any existing ones.
        self.promotions[product_id] = promo

    def remove_promo(self, product_id: int) -> None:
        if product_id not in self.promotions:
            return

        del self.promotions[product_id]

    def checkout(self, cart: Cart) -> None:
        if not cart.items:
            raise NotEnoughCartItem()

        for cart_item in cart.items.values():
            inventory_item = self.inventory.items.get(cart_item.product.product_id)
            if not inventory_item or inventory_item.count < cart_item.count:
                raise NotEnoughInventoryItem()

        receipt = Receipt()
        original_total_price = 0
        final_total_price = 0
        for cart_item in cart.items.values():
            product = cart_item.product
            self.inventory.remove_item(product=product, count=cart_item.count)

            total_price = cart_item.total_price
            original_total_price += total_price

            receipt_item = ReceiptItem(
                product_name=product.name,
                price=product.price,
                count=cart_item.count,
                original_total=total_price,
                final_total=total_price,
            )
            receipt.add_item(item=receipt_item)

            promo = self.promotions.get(product.product_id, None)
            if promo:
                total_price = promo.apply_promotion(
                    count=cart_item.count, product_price=product.price
                )
                receipt_item.final_total = total_price

            final_total_price += total_price

        receipt.original_total = original_total_price
        receipt.final_total = final_total_price

        cart.empty_cart()
        print(f"[*] Checkout Successful!\n\n{receipt}\n")


def test() -> None:
    print(store_name)
    locale = "en_GB"
    fuji_apple = Product(product_id=1, name="Fuji Apple", price=2.5)
    gala_apple = Product(product_id=2, name="Gala Apple", price=3)
    milk = Product(product_id=3, name="Milk", price=4.99)
    coke = Product(product_id=4, name="Coke", price=2)
    soup = Product(product_id=5, name="Soup", price=0.65)

    inventory = Inventory()
    inventory.add_item(product=fuji_apple, count=10)
    inventory.add_item(product=gala_apple, count=100)
    inventory.add_item(product=soup, count=500)
    inventory.add_item(product=milk, count=50)
    inventory.add_item(product=coke)
    inventory.add_item(product=coke)
    inventory.add_item(product=coke)

    print(f"{inventory}\n")
    print("=======" * 10)
    fuji_discount_promo = DiscountPromotion(
        name="Fuji 30% Discount!", discount_percentage=30
    )
    gala_discount_promo = DiscountPromotion(
        name="Gala 50% Discount!", discount_percentage=50
    )
    milk_buy_one_get_3_promo = BuyOneGetXPromotion(
        name="Buy One Milk and Get Three!", x=3
    )

    checkout_manager = CheckoutManager(inventory=inventory)
    checkout_manager.add_promo(
        product_id=fuji_apple.product_id, promo=fuji_discount_promo
    )
    checkout_manager.add_promo(
        product_id=gala_apple.product_id, promo=gala_discount_promo
    )
    checkout_manager.add_promo(
        product_id=milk.product_id, promo=milk_buy_one_get_3_promo
    )

    cart = Cart()
    cart.add_item(product=fuji_apple)
    cart.add_item(product=soup)
    cart.add_item(product=fuji_apple, count=3)
    cart.add_item(product=gala_apple, count=5)
    cart.add_item(product=milk, count=10)
    cart.add_item(product=coke)
    cart.add_item(product=coke)
    cart.add_item(product=coke)
    print(f"{cart}\n")

    cart.remove_item(product=coke)
    print(f"{cart}\n")

    cart.remove_item(product=coke, count=2)
    print(f"{cart}\n")

    gala_apple.price = 1
    print(f"{cart}\n")
    cart.recalculate_total_prices()
    print(f"{cart}\n")

    cart.delete_item(product=milk)
    print(f"{cart}\n")

    cart.add_item(product=milk, count=9)
    checkout_manager.checkout(cart=cart)

    print(f"{cart}\n")
    print(f"{inventory}\n")
    print("=======" * 10)


if __name__ == "__main__":
    test()
