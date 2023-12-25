import datetime


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

    def __str__(self) -> str:
        result = (
            f"Cart - ({datetime.datetime.now()})\n----\n"
            + "\n".join(str(item) for item in self.items.values())
            + f" \nTotal Price: {currency(self.total_price):<20s}"
        )
        return result


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
            f"{self.product_name:<12}: {currency(self.price):<7s} * {self.count:<2d}| "
            f" Original: {currency(self.original_total):<12s}"
            f" => Final: {currency(self.final_total):<12s}"
        )


class Receipt:
    def __init__(self) -> None:
        self.items: list[ReceiptItem] = []
        self.original_total = 0
        self.final_total = 0
        self.offers_msg = []
        self.no_offers_msg = "(No offers available)"

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

    def msg(self) -> str:
        msg = "\n".join(self.offers_msg) if self.offers_msg else self.no_offers_msg
        result = (
            f"\nSubtotal: {currency(self.original_total)}\n"
            + msg
            + f"\nTotal price: {currency(self.final_total)}\n"
        )
        return result


class Offer:
    def __init__(self, name: str) -> None:
        self.name = name

    def apply(self, count: int, product_price: float):
        raise NotImplementedError()


class DiscountOffer(Offer):
    def __init__(self, name: str, discount_percentage: float) -> None:
        super().__init__(name=name)
        self.multiplier = 1 - discount_percentage / 100

    def apply(self, count: int, product_price: float, cart: Cart = None):
        actual = count * product_price
        final = count * product_price * self.multiplier
        msg = f"{self.name}: {actual - final:<4.2f}"
        return final, msg


class ConditionalOffer(Offer):
    def __init__(
        self, name: str, discount_percentage: float, product_count: int, product_id: int
    ) -> None:
        super().__init__(name=name)
        self.multiplier = 1 - discount_percentage / 100
        self.product_id = product_id
        self.product_count = product_count

    def apply(self, count: int, product_price: float, cart: Cart):
        cond_count = [
            cart_item.count
            for cart_item in cart.items.values()
            if cart_item.product.product_id == self.product_id
        ]
        if not cond_count:
            return count * product_price, ""
        cond_count = cond_count[0]
        if cond_count < self.product_count:
            return count * product_price, ""
        discount_count = int(cond_count / self.product_count)
        actual = count * product_price
        final = (
            discount_count * product_price * self.multiplier
            + (count - discount_count) * product_price
        )
        msg = f"{self.name}: {actual - final:<4.2f}"
        return final, msg


class CheckoutManager:
    def __init__(self, inventory: Inventory) -> None:
        self.inventory = inventory
        self.offer: dict[int, Offer] = dict()

    def add_offer(self, product_id: int, offer: Offer) -> None:
        # Product does not need to exist in the inventory since the user may add the offer first.
        # Latest offer overrides any existing ones.
        self.offer[product_id] = offer

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

            offer = self.offer.get(product.product_id, None)
            if offer:
                total_price, msg = offer.apply(
                    count=cart_item.count, product_price=product.price, cart=cart
                )
                if total_price:
                    receipt_item.final_total = total_price
                if msg:
                    receipt.offers_msg.append(msg)

            final_total_price += total_price

        receipt.original_total = original_total_price
        receipt.final_total = final_total_price

        cart.empty_cart()
        print(f"{receipt.msg()}")


def test() -> None:
    # Products
    soup = Product(product_id=1, name="Soup", price=0.65)
    bread = Product(product_id=2, name="Bread", price=0.8)
    milk = Product(product_id=3, name="Milk", price=1.30)
    apple = Product(product_id=4, name="Apples", price=1)

    # Inventory
    inventory = Inventory()
    inventory.add_item(product=bread, count=50)
    inventory.add_item(product=apple, count=20)
    inventory.add_item(product=soup, count=40)
    inventory.add_item(product=milk, count=25)

    # Offer
    apple_discount_offer = DiscountOffer(name="Apples 10% off", discount_percentage=10)
    bread_cond_discount_offer = ConditionalOffer(
        name="Buy 2 Soup Get Bread 50% off",
        discount_percentage=50,
        product_count=2,
        product_id=soup.product_id,
    )

    checkout_manager = CheckoutManager(inventory=inventory)
    checkout_manager.add_offer(product_id=apple.product_id, offer=apple_discount_offer)
    checkout_manager.add_offer(
        product_id=bread.product_id, offer=bread_cond_discount_offer
    )

    # Cart
    cart = Cart()
    cart.add_item(product=apple)
    cart.add_item(product=bread)
    cart.add_item(product=milk)
    print(cart)
    checkout_manager.checkout(cart=cart)
    print("=======" * 10)

    # Cart
    cart = Cart()
    cart.add_item(product=milk)
    print(cart)
    checkout_manager.checkout(cart=cart)
    print("=======" * 10)

    # Cart
    cart = Cart()
    cart.add_item(product=apple)
    cart.add_item(product=bread)
    cart.add_item(product=milk)
    cart.add_item(product=bread, count=2)
    cart.add_item(product=soup, count=4)
    print(cart)
    checkout_manager.checkout(cart=cart)
    print("=======" * 10)

    # Cart
    cart = Cart()
    cart.add_item(product=bread, count=2)
    cart.add_item(product=soup, count=2)
    print(cart)
    checkout_manager.checkout(cart=cart)
    print("=======" * 10)

    # Cart
    cart = Cart()
    cart.add_item(product=apple, count=2)
    print(cart)
    checkout_manager.checkout(cart=cart)
    print("=======" * 10)
    print(inventory.items)


if __name__ == "__main__":
    test()
