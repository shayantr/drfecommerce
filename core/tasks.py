from celery import shared_task


@shared_task(bind=True)
def hold_order_status(self, order_id):
    from core.models import UserOrder
    from core.models.order import OrderStatus, Order
    from core.models.payment import PaymentStatus, Payment
    from order.service import restore_product_reservation
    user_order = UserOrder.objects.get(id=order_id)
    payment = Payment.objects.filter(order=user_order, status=PaymentStatus.PAID)
    if payment.exists():
        pass
    else:
        user_order.status = OrderStatus.CANCELLED
        user_order.save()
        items = Order.objects.filter(order=user_order)
        for item in items:
            restore_product_reservation(item)


# @shared_task(bind=True, max_retries=3)
# def verify_payment(self, payment):
#     order = UserOrder.objects.get(id=payment.order.id)
#
#     try:
#         # call gateway verify API
#         if payment.status == PaymentStatus.PAID:
#             order.status = OrderStatus.PAID
#         else:
#             order.status = OrderStatus.CANCELLED
#             # release_reserved_products(order)
#
#         order.save()
#
#     except Exception as e:
#         raise self.retry(exc=e, countdown=60)