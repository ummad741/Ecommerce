from django.db import models
from django.core.validators import RegexValidator
from Admins.models import *
# CHOOISES
viloyatlar = (
    ('Toshkent', "Toshkent"),
    ('Namangan', "Namangan"),
    ('Navoiy', "Navoiy"),
    ('Buxoro', "Buxoro"),
    ('Qashqadaryo', "Qashqadaryo"),
)

payment_ch = (
    ("cash", "cash"),
    ("credit", "credit")
)

time_ch = (
    (3, 3),
    (6, 6),
    (12, 12)
)

status = (
    ("Buyurtma qabul qilindi", "Buyurtma qabul qilindi"),
    ('Buyurtma bekor qilindi', 'Buyurtma bekor qilindi'),
    ("Buyurtma Tayorlanmoqda", "Buyurtma Tayorlanmoqda"),
    ("Buyurtma Yetkazildi", "Buyurtma Yetkazildi"),
)
# Create your models here.


class Users (models.Model):
    name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=100, null=True)
    phone_regex = RegexValidator(
        regex='d{0,9}', message="Telefon raqamini +998xxxxxxxxx kabi kriting")
    phone = models.CharField(
        validators=[phone_regex], max_length=9, unique=True
    )
    password = models.CharField(max_length=255, null=True)
    otp = models.CharField(max_length=4, null=True)
    # bank schet kredit bolsa generatsiya qilib beradi
    idp = models.CharField(max_length=8, null=True)
    seria = models.CharField(max_length=2, null=True)
    raqam = models.CharField(max_length=7, null=True)
    pasport = models.FileField(
        upload_to="uploads/pasports", null=True, blank=True)
    image = models.ImageField(upload_to="uploads/image", null=True, blank=True)
    card = models.CharField(max_length=4, null=True,
                            blank=True)  # amal qilish mudati
    card_number = models.CharField(max_length=16, null=True, blank=True)
    addres = models.TextField()

    viloyat = models.CharField(
        max_length=30, null=True, choices=viloyatlar, blank=True, default="Toshkent")

    def __str__(self):
        return f"id:{self.pk}  phone:{self.phone}"


class Orders(models.Model):

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # sotib olindi bosa true or false
    is_buy = models.BooleanField(default=False, null=True, blank=True)
    # maxsulot savatda bor bosa True or False
    in_basket = models.BooleanField(default=False, null=True, blank=True)
    quantity = models.IntegerField(default=0,)
    payment = models.CharField(choices=payment_ch, max_length=8, blank=True)
    period = models.IntegerField(choices=time_ch, null=True, blank=True)
    status = models.CharField(choices=status, max_length=30, blank=True)

    def __str__(self):
        return f"id:{self.pk}  phone:{self.user}"
# card + bosilganda is_buy true boladi va korzinkaga tushadi qachon tolov bogandan keyin status buyurtma qabul qilindiga aylanadi viloyat bizaga uzoroda bosa kun kopro berilishi mumkun
