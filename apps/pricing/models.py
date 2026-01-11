from django.db import models

from common import BaseModel


class Pricing(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.title


    class Meta:
        db_table = 'pricing'
        ordering = ['-created_at']
