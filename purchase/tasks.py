from celery import shared_task
from django.apps import apps

from core.models.order import OrderStatus
from purchase.gatway import ZarinGatWay
from purchase.service import restore_product_reservation
UserOrder = apps.get_model('core', 'UserOrder')
Order = apps.get_model('core', 'Order')
Payment = apps.get_model('core', 'Payment')



@shared_task(bind=True)
def hold_order_status(self, order_id):
    from core.models.payment import PaymentStatus

    user_order = UserOrder.objects.get(id=order_id)
    payment = Payment.objects.filter(order=user_order, status=PaymentStatus.PAID)
    if payment.exists():
        user_order.status = OrderStatus.PENDING
        user_order.save()
    else:
        user_order.status = OrderStatus.CANCELLED
        user_order.save()
        items = Order.objects.filter(order=user_order)
        for item in items:
            restore_product_reservation(item)


@shared_task(bind=True)
def verify_payment(self, payment):
    from core.models.payment import PaymentStatus

    try:
        if payment.filter(status=PaymentStatus.PENDING).exists():
            gateway = ZarinGatWay(order=payment.order)
            result = gateway.verify(authority=payment.transaction_id)
            payment.status = result
            payment.save(update_fields=['status'])
            if payment.status == PaymentStatus.PAID:
                order = UserOrder.objects.get(id=payment.order.id)
                order.status = OrderStatus.PENDING
                order.save(update_fields=['status'])

    except Exception as e:
        raise self.retry(exc=e, countdown=60)