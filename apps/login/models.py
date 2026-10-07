from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    BARANGAY_CHOICES = [
        ("Adlaon", "Adlaon"),
        ("Agsungot", "Agsungot"),
        ("Anas", "Anas"),
        ("Babag", "Babag"),
        ("Bacayan", "Bacayan"),
        ("Banilad", "Banilad"),
        ("Basak Pardo", "Basak Pardo"),
        ("Basak San Nicolas", "Basak San Nicolas"),
        ("Binaliw", "Binaliw"),
        ("Bonbon", "Bonbon"),
        ("Budla-an", "Budla-an"),
        ("Buhisan", "Buhisan"),
        ("Bulacao", "Bulacao"),
        ("Buot-Taup Pardo", "Buot-Taup Pardo"),
        ("Busay", "Busay"),
        ("Calamba", "Calamba"),
        ("Cambinocot", "Cambinocot"),
        ("Camputaw", "Camputaw"),
        ("Capitol Site", "Capitol Site"),
        ("Carreta", "Carreta"),
        ("Central", "Central"),
        ("Cogon Pardo", "Cogon Pardo"),
        ("Cogon Ramos", "Cogon Ramos"),
        ("Day-as", "Day-as"),
        ("Duljo", "Duljo"),
        ("Ermita", "Ermita"),
        ("Guadalupe", "Guadalupe"),
        ("Guba", "Guba"),
        ("Hipodromo", "Hipodromo"),
        ("Inayawan", "Inayawan"),
        ("Kalubihan", "Kalubihan"),
        ("Kalinasan", "Kalinasan"),
        ("Kamagayan", "Kamagayan"),
        ("Kasambagan", "Kasambagan"),
        ("Kinasang-an Pardo", "Kinasang-an Pardo"),
        ("Labangon", "Labangon"),
        ("Lahug", "Lahug"),
        ("Lorega", "Lorega"),
        ("Lusaran", "Lusaran"),
        ("Luz", "Luz"),
        ("Mabini", "Mabini"),
        ("Mabolo", "Mabolo"),
        ("Malubog", "Malubog"),
        ("Mambaling", "Mambaling"),
        ("Pahina Central", "Pahina Central"),
        ("Pahina San Nicolas", "Pahina San Nicolas"),
        ("Pamutan", "Pamutan"),
        ("Pardo", "Pardo"),
        ("Pari-an", "Pari-an"),
        ("Paril", "Paril"),
        ("Pasil", "Pasil"),
        ("Pit-os", "Pit-os"),
        ("Pulangbato", "Pulangbato"),
        ("Pung-ol-Sibugay", "Pung-ol-Sibugay"),
        ("Punta Princesa", "Punta Princesa"),
        ("Quiot Pardo", "Quiot Pardo"),
        ("Sambag I", "Sambag I"),
        ("Sambag II", "Sambag II"),
        ("San Antonio", "San Antonio"),
        ("San Jose", "San Jose"),
        ("San Nicolas Central", "San Nicolas Central"),
        ("San Roque", "San Roque"),
        ("Santa Cruz", "Santa Cruz"),
        ("Sapangdaku", "Sapangdaku"),
        ("Sawang Calero", "Sawang Calero"),
        ("Sinsin", "Sinsin"),
        ("Sirao", "Sirao"),
        ("Suba Pob.", "Suba Pob."),
        ("Sudlon I", "Sudlon I"),
        ("Sudlon II", "Sudlon II"),
        ("T. Padilla", "T. Padilla"),
        ("Tabunan", "Tabunan"),
        ("Tagbao", "Tagbao"),
        ("Talamban", "Talamban"),
        ("Taptap", "Taptap"),
        ("Tejero", "Tejero"),
        ("Tinago", "Tinago"),
        ("Tisa", "Tisa"),
        ("To-ong Pardo", "To-ong Pardo"),
        ("Zapatera", "Zapatera"),
    ]
    
    email = models.EmailField(unique=True)
    is_resident = models.BooleanField(default=True)
    is_lgu_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    barangay = models.CharField(
        max_length=100,
        choices=BARANGAY_CHOICES,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        role = "Staff" if self.is_lgu_staff else "Resident"
        return f"{self.email}: {role}"