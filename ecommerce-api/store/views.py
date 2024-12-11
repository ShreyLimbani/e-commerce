from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from .models import Cart, DiscountCode, Item, Order, OrderItem
from .serializers import ItemSerializer, CartSerializer, DiscountCodeSerializer
import uuid
from ecommerce.settings import DEFAULT_DISCOUNT_ORDER_COUNT

@api_view(['POST'])
def add_item(request):
    """
    Admin endpoint to add a new item to the catalog.
    """
    item_id = request.data.get('item_id')
    name = request.data.get('name')
    description = request.data.get('description', "")
    price = request.data.get('price')

    if not (item_id and name and price):
        return Response({"message": "Item ID, Name, and Price are required."}, status=400)

    try:
        # Create the new item
        item, created = Item.objects.get_or_create(
            item_id=item_id,
            defaults={
                "name": name,
                "description": description,
                "price": float(price),
            },
        )

        if created:
            # Use ItemSerializer to return a response
            serializer = ItemSerializer(item)
            return Response({"message": f"Item '{name}' added successfully.", "item": serializer.data})
        else:
            return Response({"message": "Item with this ID already exists."}, status=400)
    except Exception as e:
        return Response({"message": f"Error: {str(e)}"}, status=500)


@api_view(['GET'])
def list_items(request):
    """
    Lists all items in the catalog.
    """
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data, status=200)


@api_view(['POST'])
def add_to_cart(request):
    """
    Adds an item to the user's cart.
    """
    user_id = request.data.get('user_id')
    item_id = request.data.get('item_id')
    quantity = int(request.data.get('quantity', 1))

    try:
        # Fetch the item
        item = Item.objects.get(item_id=item_id)

        # Add to cart
        cart_item, created = Cart.objects.get_or_create(user_id=user_id, item=item)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        cart_serializer = CartSerializer(cart_item)

        return Response({
            "message": f"Added {quantity} of '{item.name}' to the cart.",
            "cart": cart_serializer.data
        })
    except Item.DoesNotExist:
        return Response({"message": "Item does not exist."}, status=404)
    except Exception as e:
        return Response({"message": f"Error: {str(e)}"}, status=500)


@api_view(['GET'])
def view_cart(request, user_id):
    """
    Fetches all items in the user's cart.
    """
    cart_items = Cart.objects.filter(user_id=user_id)

    if not cart_items.exists():
        return Response({"message": "Your cart is empty.", "cart":[], "amount":0})

    cart_serializer = CartSerializer(cart_items, many=True)
    
    total_amount = sum(cart_item['quantity'] * cart_item['item']['price'] for cart_item in cart_serializer.data)

    return Response({
        "message": f"Your cart has {len(cart_items)} items.",
        "cart": cart_serializer.data,
        "total_amount": total_amount
    })


@api_view(['POST'])
def checkout(request):
    """
    Processes the user's cart and creates an order.
    """
    user_id = request.data.get('user_id')
    discount_code_input = request.data.get('discount_code')

    # Fetch cart items
    cart_items = Cart.objects.filter(user_id=user_id)
    if not cart_items.exists():
        return Response({"message": "Cart is empty."}, status=400)

    # Calculate total price
    total_amount = sum(cart_item.quantity * cart_item.item.price for cart_item in cart_items)
    discount_amount = 0
    discount_code = None

    # Validate discount code
    if discount_code_input:
        try:
            discount_code = DiscountCode.objects.get(code=discount_code_input, is_valid=True)
            discount_amount = total_amount * (discount_code.discount_percentage / 100)
            discount_code.is_valid = False  # Invalidate the code
            discount_code.save()
        except DiscountCode.DoesNotExist as e:
            return Response({"message": "Invalid or expired discount code."}, status=400)

    # Final total
    final_amount = total_amount - discount_amount

    # Create order
    order = Order.objects.create(
        user_id=user_id,
        total_amount=final_amount,
        discount_amount=discount_amount,
        discount_code=discount_code
    )

    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            item_id=cart_item.item.item_id,
            quantity=cart_item.quantity,
            price=cart_item.item.price
        )

    # Clear cart
    cart_items.delete()

    # Generate a new discount code for every nth order
    new_discount_code = None
    if Order.objects.count() % DEFAULT_DISCOUNT_ORDER_COUNT == 0:
        new_discount_code = str(uuid.uuid4())[:8].upper()
        DiscountCode.objects.create(code=new_discount_code)

    return Response({
        "message": "Order placed successfully.",
        "order_id": order.id,
        "final_amount": final_amount,
        "new_discount_code": new_discount_code
    })

@api_view(['POST'])
def generate_discount_code(request):
    """
    Generates a new discount code.
    """
    discount_percentage = request.data.get("discount_percentage")

    code = str(uuid.uuid4())[:8].upper()  # Generate an 8-character code
    DiscountCode.objects.create(code=code, is_valid=True, discount_percentage=discount_percentage)

    return Response({"message": "Discount code generated.", "code": code})


@api_view(['GET'])
def view_purchase_summary(request):
    """
    Provides a summary of purchases and discounts.
    Optimized to minimize database queries.
    """
    # Aggregate total_orders, total_revenue, and total_discount in a single query
    order_summary = Order.objects.aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('total_amount'),
        total_discount=Sum('discount_amount')
    )

    # Fetch all discount codes in one query
    discount_codes = DiscountCode.objects.all()
    discount_code_serializer = DiscountCodeSerializer(discount_codes, many=True)

    return Response({
        "total_orders": order_summary.get("total_orders", 0),
        "total_revenue": order_summary.get("total_revenue", 0.0),
        "total_discount": order_summary.get("total_discount", 0.0),
        "discount_codes": discount_code_serializer.data
    })
