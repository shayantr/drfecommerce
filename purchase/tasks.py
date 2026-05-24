from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.apps import apps

from core.models.order import OrderStatus
from purchase.service.product_services import restore_product_reservation
from purchase.service.zarin_gateway import ZarinGatWay

UserOrder = apps.get_model('core', 'UserOrder')
Order = apps.get_model('core', 'Order')
Payment = apps.get_model('core', 'Payment')



@shared_task(bind=True)
def check_order_status(self, order_id):
    from core.models.payment import PaymentStatus
    user_order = UserOrder.objects.get(id=order_id)
    payment = Payment.objects.filter(user_order=user_order, status=PaymentStatus.PAID)
    if payment.exists():
        user_order.status = OrderStatus.PENDING
        user_order.save(update_fields=['status'])
    else:
        user_order.status = OrderStatus.CANCELLED
        user_order.save()
        items = Order.objects.filter(user_order=user_order)
        for item in items:
            restore_product_reservation(item)


@shared_task(bind=True, max_retries=2, default_retry_delay=60)
def verify_payment(self, payment_id):
    from core.models.payment import PaymentStatus
    try:
        payment = Payment.objects.select_related('user_order').get(id=payment_id)
        if payment.status != PaymentStatus.PENDING:
            return None
        gateway = ZarinGatWay(order=payment.user_order)
        result = gateway.verify(authority=payment.transaction_id)
        if result['success']:
            payment.status = PaymentStatus.PAID
            payment.save(update_fields=['status'])
            payment.user_order.status = OrderStatus.PENDING
            payment.user_order.save(update_fields=['status'])
            return None
        payment.status = PaymentStatus.FAILED
        payment.save(update_fields=['status'])

    except Exception as e:
        try:
            raise self.retry(exc=e, countdown=60)
        except MaxRetriesExceededError:
            if payment:
                payment.status = PaymentStatus.FAILED
                payment.save(update_fields=['status'])