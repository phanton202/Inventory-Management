from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name