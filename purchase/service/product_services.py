from core.models import Product


def restore_product_reservation(item):
    product = Product.objects.select_for_update().filter(pk=item.product.pk).first()
    product.quantity += item.quantity
    product.save()

