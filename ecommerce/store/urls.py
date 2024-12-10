from django.urls import path
from .views import add_item, add_to_cart, checkout, generate_discount_code, list_items, view_purchase_summary, view_cart

urlpatterns = [
    path('api/cart/add/', add_to_cart, name='add_to_cart'),
    path('api/cart/view/<str:user_id>/', view_cart, name='view_cart'),
    path('api/cart/checkout/', checkout, name='checkout'),
    path('api/items/', list_items, name='list_items'),
    path('api/admin/add-item/', add_item, name='add_item'),
    path('api/admin/generate-discount/', generate_discount_code, name='generate_discount_code'),
    path('api/admin/stats/', view_purchase_summary, name='view_purchase_summary'),
]
