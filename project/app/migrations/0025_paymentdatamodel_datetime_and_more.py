# Generated by Django 5.0.6 on 2024-06-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_remove_paymentdatamodel_datetime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentdatamodel',
            name='Datetime',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='paymentdatamodel',
            name='Created_at',
            field=models.CharField(max_length=255, null=True),
        ),
    ]