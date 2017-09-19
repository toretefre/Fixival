from django.db import models

# Create your models here.

class Konserter(models.Model):
    scene = models.CharField(max_length=200)
    teknikere= models.TextField()
    konsert = models.CharField(max_length=200)
    dato = models.DateTimeField(blank=True, null=True)
    band = models.CharField(max_length=200)
    festival = models.CharField(max_length=200)
