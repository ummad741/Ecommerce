from django.db import models
from django.core.validators import RegexValidator

# CHOOISES
viloyatlar = (
    ('Toshkent', "Toshkent"),
    ('Namangan', "Namangan"),
    ('Navoiy', "Navoiy"),
    ('Buxoro', "Buxoro"),
    ('Qashqadaryo', "Qashqadaryo"),
)




# Create your models here.


class Users (models.Model):
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    phone_regex = RegexValidator(
        regex='d{0,9}', message="Telefon raqamini +998xxxxxxxxx kabi kriting")
    phone = models.CharField(
        validators=[phone_regex], max_length=9, unique=True)
    password = models.CharField(max_length=20, null=True)
    otp = models.CharField(max_length=4, null=True)
    # bank schet kredit bolsa generatsiya qilib beradi
    idp = models.CharField(max_length=8, null=True)
    seria = models.CharField(max_length=2, null=True)
    raqam = models.CharField(max_length=7, null=True)
    pasport = models.FileField(
        upload_to="uploads/pasports", null=True, blank=True)
    image = models.FileField(upload_to="uploads/image", null=True, blank=True)
    card = models.CharField(max_length=4, null=True,
                            blank=True)  # amal qilish mudati
    card_number = models.CharField(max_length=20, null=True, blank=True)
    addres = models.TextField()

    viloyat = models.CharField(
        max_length=30, null=True, choices=viloyatlar, blank=True, default="Toshkent")

    def __str__(self):
        return f"id:{self.pk}  phone:{self.phone}"
