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


class Product(models.Model):
    categ = (
        ('Elektronika', 'Elektronika'),
        ('Maishiy_texnika', 'Maishiy_texnika'),
        ('Noutbooklar', 'Noutbooklar'),
        ('Smartfonlar', 'Smartfonlar'),
        ('Planshetlar', 'Planshetlar')
    )
    # shotda title bilan tableni ulab ketsa boladi lekin keyinchali update qilishim mumkun
    title = models.CharField(max_length=250, null=True, unique=True)
    description = models.TextField(null=True)
    quantity = models.IntegerField(null=True)
    protsent = models.IntegerField(default=0)
    cost = models.IntegerField(null=True)
    category = models.CharField(max_length=250, choices=categ, null=True)
    color = models.CharField(max_length=13, null=True)
    image = models.ImageField(upload_to='uploads/rasmlar/', null=True)
    time = models.DateTimeField(auto_now=True)

    admin = models.ForeignKey(Admins, on_delete=models.CASCADE)

    def str(self):
        return self.name
