from django.db import models

# Create your models here.

class Konserter(models.Model):
    scene = models.CharField(max_length=200)
    teknikere= models.TextField()
    konsert = models.CharField(max_length=200)
    dato = models.DateTimeField(blank=True, null=True)
    band = models.CharField(max_length=200)
    festival = models.CharField(max_length=200)

class Band(models.Model):
    navn = models.CharField(max_length=200)
    kostnad = models.IntegerField()
    manager = models.ForeignKey('auth.User')
    utstyr = models.TextField()
    sjanger = models.CharField(max_length=100)
    info = models.TextField()
    rating = models.IntegerField()

class Bestilling(models.Model):
    dato = models.DateTimeField(blank=True,null=True)
    band = models.ForeignKey('models.Band')
    scene = models.CharField(max_length=200)
    godkjent = models.CharField(max_length=3)
