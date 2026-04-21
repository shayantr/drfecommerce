from django.urls import path

from product.api.admin_product import CreateProductApiView

urlpatterns = [
    path('create/', CreateProductApiView.as_view()),
]

