# Generated by Django 4.2.13 on 2024-05-24 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_indexcarousel_productbox'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationmodel',
            name='About',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='registrationmodel',
            name='Profile',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='registrationmodel',
            name='Email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
