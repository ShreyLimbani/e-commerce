from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from .models import Item, Cart, Order, OrderItem, DiscountCode

class BaseTestCase(TestCase):
    """Base test class for shared setup logic."""
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()


class ItemTests(BaseTestCase):
    """Test cases for item-related endpoints."""

    def test_add_item_success(self):
        """Test successful addition of an item."""
        url = reverse('add_item')
        data = {
            'item_id': 'ITEM123',
            'name': 'Laptop',
            'price': 1200.0,
            'description': 'A high-performance laptop'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "added successfully")
        self.assertTrue(Item.objects.filter(item_id='ITEM123').exists())

    def test_add_item_missing_fields(self):
        """Test adding an item with missing required fields."""
        url = reverse('add_item')
        data = {'name': 'Phone', 'price': 800.0}  # Missing 'item_id'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Item ID, Name, and Price are required.")

    def test_list_items(self):
        """Test listing all items in the catalog."""
        Item.objects.create(item_id='ITEM123', name='Phone', price=600.0, description='A smartphone')
        url = reverse('list_items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Phone')


class CartTests(BaseTestCase):
    """Test cases for cart-related endpoints."""

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(item_id='ITEM123', name='Tablet', price=300.0)

    def test_add_to_cart_success(self):
        """Test successfully adding an item to the cart."""
        url = reverse('add_to_cart')
        data = {'user_id': 'user1', 'item_id': self.item.item_id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Added 2 of 'Tablet' to the cart.")
        self.assertTrue(Cart.objects.filter(user_id='user1', item=self.item).exists())

    def test_view_empty_cart(self):
        """Test viewing an empty cart."""
        url = reverse('view_cart', args=['user1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart is empty.")

    def test_view_cart_with_items(self):
        """Test viewing a cart with items."""
        Cart.objects.create(user_id='user1', item=self.item, quantity=3)
        url = reverse('view_cart', args=['user1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your cart has 1 items.")
        self.assertContains(response, f"Tablet")


class CheckoutTests(BaseTestCase):
    """Test cases for checkout functionality."""

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(item_id='ITEM123', name='Camera', price=500.0)
        cls.discount_code = DiscountCode.objects.create(code='DISCOUNT10', discount_percentage=10, is_valid=True)

    def test_checkout_without_discount(self):
        """Test successful checkout without a discount code."""
        Cart.objects.create(user_id='user1', item=self.item, quantity=2)
        url = reverse('checkout')
        data = {'user_id': 'user1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order placed successfully.")
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_checkout_with_discount(self):
        """Test successful checkout with a discount code."""
        Cart.objects.create(user_id='user1', item=self.item, quantity=2)
        url = reverse('checkout')
        data = {'user_id': 'user1', 'discount_code': self.discount_code.code}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order placed successfully.")
        self.assertEqual(response.data['final_amount'], 900.0)  # 10% discount applied

    def test_checkout_invalid_discount(self):
        """Test checkout with an invalid discount code."""
        Cart.objects.create(user_id='user1', item=self.item, quantity=2)
        url = reverse('checkout')
        data = {'user_id': 'user1', 'discount_code': 'INVALID'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], "Invalid or expired discount code.")


class AdminTests(BaseTestCase):
    """Test cases for admin endpoints."""

    def test_generate_discount_code(self):
        """Test that a discount code is generated successfully."""
        url = reverse('generate_discount_code')
        data = {'discount_percentage': 15}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Discount code generated.")
        self.assertTrue(DiscountCode.objects.exists())

    def test_view_purchase_summary(self):
        """Test the purchase summary view."""
        item = Item.objects.create(item_id='ITEM123', name='Speaker', price=150.0)
        order = Order.objects.create(user_id='user1', total_amount=150.0, discount_amount=10.0)
        OrderItem.objects.create(order=order, item_id=item.item_id, quantity=1, price=item.price)
        
        url = reverse('view_purchase_summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "total_orders")
        self.assertContains(response, "total_revenue")
        self.assertContains(response, "total_discount")


class IntegrationTests(BaseTestCase):
    """End-to-end tests combining multiple endpoints."""

    def test_full_order_process(self):
        """Test the full process: add item, add to cart, checkout."""
        # Add an item
        item = Item.objects.create(item_id='ITEM123', name='Monitor', price=250.0)
        
        # Add item to cart
        add_cart_url = reverse('add_to_cart')
        cart_data = {'user_id': 'user1', 'item_id': item.item_id, 'quantity': 2}
        response = self.client.post(add_cart_url, cart_data, format='json')
        self.assertEqual(response.status_code, 200)

        # Checkout
        checkout_url = reverse('checkout')
        checkout_data = {'user_id': 'user1'}
        response = self.client.post(checkout_url, checkout_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Order placed successfully.")
