from django.urls import path

urlpatterns = [
    path('api/cart/add/', None),
	path('api/cart/apply-code/', None),
    path('api/cart/checkout/', None),
	path('api/admin/add-item/', None),
    path('api/admin/generate-discount/', None),
    path('api/admin/stats/', None),
]
