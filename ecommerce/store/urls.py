from django.urls import path
from .views import add_item, add_to_cart, checkout, generate_discount_code, view_purchase_summary, view_cart

urlpatterns = [
    path('api/cart/add/', add_to_cart),
	path('api/cart/view/', view_cart),
    path('api/cart/checkout/', checkout),
	path('api/admin/add-item/', add_item),
    path('api/admin/generate-discount/', generate_discount_code),
    path('api/admin/stats/', view_purchase_summary),
]
