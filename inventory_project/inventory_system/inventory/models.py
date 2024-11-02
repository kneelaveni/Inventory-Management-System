from django.db import models

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length =255)
    description = models.TextField()

    class Meta:
        db_table = 'items'