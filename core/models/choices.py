from django.db import models


class PaymentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    PAID = 2, 'Paid'
    FAILED = 3, 'Failed'

class OrderStatus(models.IntegerChoices):
    CANCELLED = 1, 'Cancelled'
    PENDING = 2, 'Pending'
    RETURNED = 3, 'Returned'
    COMPLETED = 4, 'Completed'
    DELIVERED = 5, 'Delivered'

class StockAvailability(models.IntegerChoices):
    YES = 1, 'Yes'
    NO = 2, 'No'

class AuthProviders(models.IntegerChoices):
    CUSTOMER = 1, 'Customer'
    ADMIN = 2, 'Admin'
    ACCOUNTANT = 3, 'Accountant'

