from django.db import models

# Create your models here.

class User(models.Model):
    mobile = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
