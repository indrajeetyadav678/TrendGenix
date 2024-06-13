# Generated by Django 5.0.6 on 2024-06-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_productmodel_product_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchaseproduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Purchase_date', models.DateTimeField(auto_created=True)),
                ('Product_Type', models.CharField(max_length=254, null=True)),
                ('Prod_Image1', models.ImageField(null=True, upload_to='')),
                ('Prod_Image2', models.ImageField(null=True, upload_to='')),
                ('Prod_Image3', models.ImageField(null=True, upload_to='')),
                ('Prod_Image4', models.ImageField(null=True, upload_to='')),
                ('Prod_Price', models.IntegerField(null=True)),
                ('Prod_MRP', models.IntegerField(null=True)),
                ('Prod_Offer', models.CharField(max_length=254, null=True)),
                ('Prod_Detail', models.TextField(null=True)),
                ('prod_color', models.CharField(max_length=254, null=True)),
                ('Serial_no', models.IntegerField(null=True)),
                ('Order_id', models.CharField(max_length=255, null=True)),
                ('Email_id', models.EmailField(max_length=254, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='productmodel',
            name='prod_color',
            field=models.CharField(max_length=254, null=True),
        ),
    ]