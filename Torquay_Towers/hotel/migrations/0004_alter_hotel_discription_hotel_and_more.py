# Generated by Django 4.2.1 on 2023-05-15 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_booking_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='discription_hotel',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='environment_hotel',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='location_hotel',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='name_hotel',
            field=models.CharField(max_length=50),
        ),
    ]
