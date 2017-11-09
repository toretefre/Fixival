from django.db import models
from django.core.validators import MaxValueValidator
# Create your models here.


class Band(models.Model):
    navn = models.CharField(max_length=200)
    kostnad = models.IntegerField()
    manager = models.ForeignKey('auth.User')
    utstyr = models.TextField()
    sjanger = models.CharField(default='undefined', max_length=100)
    info = models.TextField()
    rating = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    albums_sold = models.PositiveIntegerField(default=0)
    previous_concerts = models.TextField(default='Ingen')
    kontakt_info = models.TextField()

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name_plural = "Band"


class Bestilling(models.Model):
    dato = models.DateTimeField(blank=True, null=True)
    band = models.ForeignKey('Band')
    scene = models.ForeignKey('Scener')
    godkjenning = ((True, 'Godkjent'), (False, 'Ikke godkjent'), (None, 'Ikke vurdert enda'))
    godkjent = models.NullBooleanField(choices=godkjenning, default=None)
    pris = models.PositiveIntegerField()

    def __str__(self):
        return self.band.navn

    class Meta:
        verbose_name_plural = "Bestillinger"


class Konserter(models.Model):
    scene = models.ForeignKey('Scener')
    teknikere = models.ManyToManyField('auth.User', blank=True)
    konsert = models.CharField(max_length=200)
    dato = models.DateTimeField(blank=True, null=True)
    band = models.ManyToManyField(Band, blank=True)
    festival = models.CharField(max_length=200)
    # forventet antall billetter
    publikumsantall = models.PositiveIntegerField(default=0, blank=True, null=True)
    # faktisk solgte billetter, gjerne hentet fra billettsystem
    solgtebilletter = models.PositiveIntegerField(default=0, blank=True, null=True)
    billettpris = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.konsert

    class Meta:
        verbose_name_plural = "Konserter"


class Backline(models.Model):
    band = models.ForeignKey('band', models.SET_NULL, blank=True, null=True,)
    backline = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.backline


class Tekniske_behov(models.Model):
    band = models.ForeignKey('band', models.SET_NULL, blank=True, null=True,)
    backline = models.ForeignKey('backline', models.SET_NULL, blank=True, null=True,)
    behov = models.CharField(max_length=50, db_index=True)
    opplastet = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.behov)

    class Meta:
        verbose_name_plural = "Tekniske behov"


class Scener(models.Model):
    navn = models.CharField(max_length=200)
    storrelse = models.IntegerField()
    kostnad = models.IntegerField()

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name_plural = "Scener"
