from django.contrib.auth.models import User, Group
from .models import *
# Creates all users
User.objects.create(username="mrarrangoer",password="12345678o").save()
User.objects.create(username="mrpr",password="12345678o").save()
User.objects.create(username="mrbookingansvarlig",password="12345678o").save()
User.objects.create(username="mrbookingsjef",password="12345678o").save()
User.objects.create(username="mrtekniker",password="12345678o").save()
User.objects.create(username="mrtekniker2",password="12345678o").save()
User.objects.create(username="mrmanager",password="12345678o").save()
# Creates all groups
Group.objects.create(name="bookingansvarlig").user_set.add(User.objects.get(username="mrbookingansvarlig"))
Group.objects.create(name="bookingsjef").user_set.add(User.objects.get(username="mrbookingsjef"))
Group.objects.create(name="tekniker").user_set.add(User.objects.get(username="mrtekniker"),User.objects.get(username="mrtekniker2"))
Group.objects.create(name="manager").user_set.add(User.objects.get(username="mrmanager"))
Group.objects.create(name="arrangoer").user_set.add(User.objects.get(username="mrarrangoer"))
Group.objects.create(name="PR-ansvarlig").user_set.add(User.objects.get(username="mrpr"))
# Creates bands
Band.objects.create(navn="",kostnad=1000,info="",utstyr="",rating=0,albums_sold=0,kontakt_info="").manager = User.objects.get(username="mrmanager")
Band.objects.create(navn="",kostnad=1000,info="",utstyr="",rating=0,albums_sold=0,kontakt_info="").manager = User.objects.get(username="mrmanager")
Band.objects.create(navn="",kostnad=1000,info="",utstyr="",rating=0,albums_sold=0,kontakt_info="").manager = User.objects.get(username="mrmanager")
Band.objects.create(navn="",kostnad=1000,info="",utstyr="",rating=0,albums_sold=0,kontakt_info="").manager = User.objects.get(username="mrmanager")
Band.objects.create(navn="",kostnad=1000,info="",utstyr="",rating=0,albums_sold=0,kontakt_info="").manager = User.objects.get(username="mrmanager")
# Scener
Scener.objects.create(navn="",storrelse=0,kostnad=0)
Scener.objects.create(navn="",storrelse=0,kostnad=0)
Scener.objects.create(navn="",storrelse=0,kostnad=0)
Scener.objects.create(navn="",storrelse=0,kostnad=0)
# Konserter
Konserter.objects.create(konsert="",dato="2019-11-11 11:11",festival="",publikumsantall=0,solgtebilletter=0,billettpris=0)
Konserter.objects.create(konsert="",dato="2019-11-11 11:11",festival="",publikumsantall=0,solgtebilletter=0,billettpris=0)
Konserter.objects.create(konsert="",dato="2019-11-11 11:11",festival="",publikumsantall=0,solgtebilletter=0,billettpris=0)
Konserter.objects.create(konsert="",dato="2019-11-11 11:11",festival="",publikumsantall=0,solgtebilletter=0,billettpris=0)
Konserter.objects.create(konsert="",dato="2019-11-11 11:11",festival="",publikumsantall=0,solgtebilletter=0,billettpris=0)

# Henter konsertobjecter
kons1 = Konserter.objects.get(konsert="")
kons2 = Konserter.objects.get(konsert="")
kons3 = Konserter.objects.get(konsert="")
kons4 = Konserter.objects.get(konsert="")
kons5 = Konserter.objects.get(konsert="")

# Setter konsertband
kons1.band.add(Band.objects.get(navn=""),Band.objects.get(navn=""))
kons2.band.add(Band.objects.get(navn=""),Band.objects.get(navn=""))
kons3.band.add(Band.objects.get(navn=""),Band.objects.get(navn=""))
kons4.band.add(Band.objects.get(navn=""),Band.objects.get(navn=""))
kons5.band.add(Band.objects.get(navn=""),Band.objects.get(navn=""))

# Setter konsertscene
kons1.scene = Scener.objects.get(navn="")
kons2.scene = Scener.objects.get(navn="")
kons3.scene = Scener.objects.get(navn="")
kons4.scene = Scener.objects.get(navn="")
kons5.scene = Scener.objects.get(navn="")

# Setter konsertteknikere
kons1.teknikere.add(User.objects.get(username=""))
kons2.teknikere.add(User.objects.get(username=""))
kons3.teknikere.add(User.objects.get(username=""))
kons4.teknikere.add(User.objects.get(username=""))
kons5.teknikere.add(User.objects.get(username=""))

# Lagrer konsertobjectene med nye feltendringer
kons1.save()
kons2.save()
kons3.save()
kons4.save()
kons5.save()
