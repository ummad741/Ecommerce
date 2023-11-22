from django.db import models
from django.core.validators import RegexValidator

# CHOOISES
admin_roll = (
    ("Superadmin", "Superadmin"),
    ("admin", "admin"),
)

gender = (
    ("Women", "Women"),
    ("Man", "Man"),
)
# Create your models here.


class Admins(models.Model):
    admins = models.CharField(max_length=20, choices=admin_roll)
    name = models.CharField(max_length=30)
    age = models.IntegerField(default=20)
    surname = models.CharField(max_length=30)
    phone_regex = RegexValidator(
        regex='d{0,9}', message="Telefon raqamini +998xxxxxxxxx kabi kriting")
    phone = models.CharField(
        validators=[phone_regex], max_length=9, unique=True)
    password = models.CharField(max_length=16)

    gender = models.CharField(max_length=10, choices=gender)

    def __str__(self) -> str:
        return f"name:{self.name} roll: {self.admins}"
