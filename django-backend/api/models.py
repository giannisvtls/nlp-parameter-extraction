from django.db import models

class EfoTerm(models.Model):
    term = models.TextField(unique=True)

    def __str__(self):
        return self.term

class EfoTermSynonym(models.Model):
    label = models.TextField()
    efo_term = models.ForeignKey(EfoTerm, related_name='synonyms', on_delete=models.CASCADE)

    def __str__(self):
        return self.label