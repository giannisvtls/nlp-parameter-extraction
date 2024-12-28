from django.db import models

class User(models.Model):
    iban = models.TextField(unique=True)
    name = models.TextField(unique=True)
    balance = models.IntegerField()
    
    def __str__(self):
        return self.iban