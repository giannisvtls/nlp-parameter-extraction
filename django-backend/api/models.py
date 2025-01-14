from django.db import models

class Document(models.Model):
    content = models.TextField()
    embedding = models.JSONField(null=True)  # Store vector embeddings as JSON
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Document {self.id}: {self.content[:50]}..."

class User(models.Model):
    iban = models.TextField(unique=True)
    name = models.TextField(unique=True)
    balance = models.IntegerField()
    
    def __str__(self):
        return self.iban
