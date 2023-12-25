import scala.io.StdIn.readLine

def currency(value: Float, country: String = "en_GB"): String =
  if (country == "en_GB") then
    if (value >= 1) then s"£${value}"
    else s"${(value * 100).toInt}p"
  else if (country == "en_US") then
    if (value >= 1) then s"$$${value}"
    else s"${(value * 100)}c"
  else
    value.toString


abstract class GenericError(message: String) extends Exception(message)

case class NotEnoughCartItem(message: String) extends GenericError(message)

case class NotEnoughInventoryItem(message: String) extends GenericError(message)

case class InvalidInput(message: String) extends GenericError(message)

// Product
class Product(var product_id: Int, var name: String, var price: Float):

  override def toString: String =
    s"Product: $name | Price: ${currency(value = price)}"
end Product

// InventoryItem
class InventoryItem(var product: Product):
  var count: Int = 0

  def update_item_count(new_count: Int): Unit =
    if new_count == 0 then None
    else if new_count < 0 && count < new_count then
      throw new NotEnoughInventoryItem("Not enough items in the inventory")

    count += new_count

  override def toString: String =
    s"$product  | Count: $count"
end InventoryItem

// Inventory
class Inventory:
  var items: Map[Int, InventoryItem] = Map[Int, InventoryItem]()

  def add_item(product: Product, count: Int = 1): Unit =
    if count <= 0 then
      throw new InvalidInput("Count must be a positive integer.")

    if !items.contains(product.product_id) then
      items += (product.product_id -> InventoryItem(product))

    val item = items(product.product_id)
    item.update_item_count(count)

  def remove_item(product: Product, count: Int = 1): Unit =
    if count <= 0 then
      throw new InvalidInput("Count must be a positive integer.")

    val item = items(product.product_id)

    if item == null || item.count < count then
      throw new NotEnoughInventoryItem("Not enough items in the inventory")

    item.update_item_count(-count)

  def check_stock(product: Product, count: Int): Boolean =
    val item = items(product.product_id)

    if item == null || item.count < count then false
    else true

  override def toString: String =
    s"Inventory\n--------\n" + items.map { case (k, v) => v.toString }.mkString("\n")
end Inventory

// CartItem
class CartItem(var product: Product):
  var count: Int = 0
  var total_price: Float = 0

  def update_item_count(new_count: Int): Float =
    count += new_count
    var price_delta: Float = product.price * new_count
    total_price += price_delta
    price_delta

  override def toString: String =
    s"$product  | Count: $count | Total: ${currency(total_price)}\n"
end CartItem


// Cart
class Cart:
  var items: scala.collection.mutable.Map[Int, CartItem] = scala.collection.mutable.Map[Int, CartItem]()
  private var total_price: Float = 0

  def add_item(product: Product, count: Int = 1): Unit =
    if count <= 0 then
      throw new InvalidInput("Count must be a positive integer.")

    if !items.contains(product.product_id) then
      items += (product.product_id -> CartItem(product))

    val item = items(product.product_id)
    val price_delta: Float = item.update_item_count(count)
    total_price += price_delta

  private def remove_item(product: Product, count: Int = 1): Unit =
    if count <= 0 then
      throw new InvalidInput("Count must be a positive integer.")

    val item = items(product.product_id)
    if item == null || item.count < count then
      throw new NotEnoughCartItem("Not enough items in the cart")

    var price_delta: Float = item.update_item_count(-count)
    total_price += price_delta

    if item.count == 0 then
      throw new NotEnoughCartItem("Not enough items in the cart")
    else items.remove(product.product_id)

  def delete_item(product: Product): Unit =
    val item = items(product.product_id)
    if item == null then None
    else remove_item(product, count = item.count)

  def empty_cart(): Unit =
    total_price = 0
    items.clear()

  override def toString: String =
    s"Cart\n------\n" +
      items.map { case (k, v) => v.toString }.mkString("") +
      s"Cart ==>> Total Price: ${currency(total_price)}"
end Cart

// ReceiptItem
class ReceiptItem(var product_name: String,
                  var price: Float,
                  var count: Int,
                  var original_total: Float,
                  var final_total: Float):

  override def toString: String =
    s"$product_name: ${currency(price)} * $count | " +
      s" Original: ${currency(original_total)}" +
      s" => Final: ${currency(final_total)}"
end ReceiptItem


// Receipt
class Receipt:
  var items: List[ReceiptItem] = List()
  var original_total: Float = 0
  var final_total: Float = 0
  var offers_msg: List[String] = List()
  val no_offers_msg = "(No offers available)"

  def add_item(item: ReceiptItem): Unit =
    items.appended(item)

  def msg(): String =
    var new_msg: String = no_offers_msg
    if offers_msg.length > 0 then new_msg = offers_msg.mkString("\n")
    s"\nSubtotal: ${currency(original_total)}\n" + new_msg + s"\nTotal price: ${currency(final_total)}\n"

  override def toString: String =
    s"Receipt\n------\n" + items.mkString("\n") + s"\nOriginal Total: ${currency(original_total)}" +
      s" => Final Total: ${currency(final_total)}"
end Receipt


trait Offer:
  def apply(count: Int, product_price: Float, cart: Cart): (Float, String) =
    throw new NotImplementedError("Not implemented function")


class DiscountOffer(var name: String, var discount_percentage: Float) extends Offer:
  private val multiplier: Float = 1 - discount_percentage / 100

  override def apply(count: Int, product_price: Float, cart: Cart): (Float, String) =
    val actual: Float = count * product_price
    val final_value: Float = count * product_price * multiplier
    val delta: Float = actual - final_value
    val msg: String = s"$name: ${currency(delta)}"
    (final_value, msg)


class ConditionalOffer(var name: String, var discount_percentage: Float, var product_count: Int, var product_id: Int) extends Offer:
  private val multiplier: Float = 1 - discount_percentage / 100

  override def apply(count: Int, product_price: Float, cart: Cart): (Float, String) =
    var cond_count = -1
    for cart_item <- cart.items.values do
      if cart_item.product.product_id == product_id then
        cond_count = cart_item.count

    if cond_count < 0 then
      return (count * product_price, "")

    if cond_count < product_count then
      return (count * product_price, "")

    val discount_count: Int = (cond_count / product_count)
    val actual: Float = count * product_price
    val final_value: Float = discount_count * product_price * multiplier + (count - discount_count) * product_price
    val msg = s"$name: ${actual - final_value}"
    (final_value, msg)


class CheckoutManager(var inventory: Inventory):
  var offer: scala.collection.mutable.Map[Int, Offer] = scala.collection.mutable.Map[Int, Offer]()

  def add_offer(product_id: Int, new_offer: Offer): Unit =
    offer += (product_id -> new_offer)

  def checkout(cart: Cart): Unit =
    if cart.items.isEmpty then
      throw new NotEnoughCartItem("Not enough items in the cart")

    for cart_item <- cart.items.values do
      val inventory_item: InventoryItem = inventory.items(cart_item.product.product_id)
      if inventory_item == null || inventory_item.count < cart_item.count then
        throw new NotEnoughInventoryItem("Not enough items in the inventory")

    val receipt = new Receipt()
    var original_total_price: Float = 0
    var final_total_price: Float = 0

    for cart_item <- cart.items.values do
      val product = cart_item.product
      inventory.remove_item(product, cart_item.count)

      var total_price: Float = cart_item.total_price
      original_total_price += total_price

      val receipt_item = new ReceiptItem(product_name = product.name,
        price = product.price, count = cart_item.count, original_total = original_total_price, final_total = final_total_price)
      receipt.add_item(receipt_item)

      val off: Offer = offer.getOrElse(product.product_id, null)
      if off == null then None
      else
        var (total_price_new: Float, msg: String) = off.apply(count = cart_item.count, product_price = product.price, cart)
        receipt_item.final_total = total_price_new
        if !msg.isEmpty() then receipt.offers_msg = receipt.offers_msg :+ msg
        total_price = total_price_new

      final_total_price += total_price

    receipt.original_total = original_total_price
    receipt.final_total = final_total_price

    cart.empty_cart()
    println(s"${receipt.msg()}")


def test(): Unit =
  val soup = new Product(product_id = 1, name = "Soup", price = 0.65)
  val bread = new Product(product_id = 2, name = "Bread", price = 0.8)
  val milk = new Product(product_id = 3, name = "Milk", price = 1.3)
  val apple = new Product(product_id = 4, name = "Apples", price = 1);

  val inventory = new Inventory()
  inventory.add_item(product = soup, count = 10)
  inventory.add_item(product = bread, count = 30)
  inventory.add_item(product = milk, count = 20)
  inventory.add_item(product = apple, count = 40)

  val apple_discount_offer = new DiscountOffer(name = "Apples 10% off", discount_percentage = 10)
  val bread_cond_discount_offer = new ConditionalOffer(name = "Buy 2 Soup Get Bread 50% off", discount_percentage = 50,
    product_count = 2, product_id = soup.product_id)

  val checkout_manager = new CheckoutManager(inventory = inventory)
  checkout_manager.add_offer(product_id = apple.product_id, new_offer = apple_discount_offer)
  checkout_manager.add_offer(product_id = bread.product_id, new_offer = bread_cond_discount_offer)

  val cart = new Cart()
  cart.add_item(product = soup)
  cart.add_item(product = bread)
  cart.add_item(product = milk)
  println(cart)
  checkout_manager.checkout(cart = cart)
  println("=======" * 10)

  cart.add_item(product = apple)
  cart.add_item(product = soup)
  cart.add_item(product = bread)
  cart.add_item(product = milk)
  println(cart)
  checkout_manager.checkout(cart = cart)
  println("=======" * 10)

  cart.add_item(product = apple)
  cart.add_item(product = soup)
  cart.add_item(product = soup)
  cart.add_item(product = bread)
  cart.add_item(product = milk)
  println(cart)
  checkout_manager.checkout(cart = cart)
  println("=======" * 10)


@main def hello(): Unit =
  // Test Function
//  test()

  // Main Function - Apples Milk Bread Soup
  while true do
    val input = readLine("Enter the list of items.. ")
    val arr = input.split("\\W+")

    val soup = new Product(product_id = 1, name = "Soup", price = 0.65)
    val bread = new Product(product_id = 2, name = "Bread", price = 0.8)
    val milk = new Product(product_id = 3, name = "Milk", price = 1.3)
    val apple = new Product(product_id = 4, name = "Apples", price = 1);

    val inventory = new Inventory()
    inventory.add_item(product = soup, count = 10)
    inventory.add_item(product = bread, count = 30)
    inventory.add_item(product = milk, count = 20)
    inventory.add_item(product = apple, count = 40)

    val apple_discount_offer = new DiscountOffer(name = "Apples 10% off", discount_percentage = 10)
    val bread_cond_discount_offer = new ConditionalOffer(name = "Buy 2 Soup Get Bread 50% off", discount_percentage = 50,
      product_count = 2, product_id = soup.product_id)

    val checkout_manager = new CheckoutManager(inventory = inventory)
    checkout_manager.add_offer(product_id = apple.product_id, new_offer = apple_discount_offer)
    checkout_manager.add_offer(product_id = bread.product_id, new_offer = bread_cond_discount_offer)

    val cart = new Cart()
    for x <- arr do
      x.toLowerCase() match
        case "apples" =>  cart.add_item(product = apple)
        case "milk" => cart.add_item(product = milk)
        case "bread" => cart.add_item(product = bread)
        case "soup" => cart.add_item(product = soup)

    println(cart)
    checkout_manager.checkout(cart = cart)
