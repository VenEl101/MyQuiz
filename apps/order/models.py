from django.db import models
from django.db.models import TextChoices

from apps.pricing.models import Pricing
from apps.user.models import User
from common import BaseModel


class PaymentStatus(TextChoices):
    PENDING = 'PENDING', 'pending'
    COMPLETED = 'COMPLETED', 'completed'
    FAILED = 'FAILED', 'failed'


class PaymentMethod(TextChoices):
    PAYME = 'PAYME', 'payme'
    CLICK = 'CLICK', 'click'


class Order(BaseModel):
    pricing = models.ForeignKey(Pricing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)

