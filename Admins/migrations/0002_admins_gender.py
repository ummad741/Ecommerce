# Generated by Django 4.2.7 on 2023-11-21 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admins', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='admins',
            name='gender',
            field=models.CharField(choices=[('Women', 'Women'), ('Man', 'Man')], default=2, max_length=10),
            preserve_default=False,
        ),
    ]