from django.db import models

class Item(models.Model):
    """
    This models has the catalog of items for sale.
    """
    item_id  = models.CharField(max_length=50, unique=True, auto_created=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    price = models.FloatField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item: {self.name} - Price: {self.price}"


class Cart(models.Model):
    """
    This models is used to store the items added to the cart by the user.
    """
    user_id = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Cart - User: {self.user_id}, Item: {self.item.name}, Quantity: {self.quantity}"


class DiscountCode(models.Model):
    """
    This models is used to store all the discount codes generated by the system upon completion of certain orders.
    """
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.FloatField()
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Code: {self.code} - Valid: {self.is_valid}"


class Order(models.Model):
    """
    This model stores the orders received by the store.
    """
    user_id = models.CharField(max_length=50)
    total_amount = models.FloatField()
    discount_amount = models.FloatField(default=0)
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - User: {self.user_id}, Total: {self.total_amount}"


class OrderItem(models.Model):
    """
    This model stores all the items ordered in a particular order.
    Used to give us the items purchased in a order.
    """
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item_id = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return f"OrderItem - Order: {self.order.id}, Item: {self.item_id}, Quantity: {self.quantity}"
