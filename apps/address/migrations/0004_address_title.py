# Generated by Django 4.0.3 on 2022-05-19 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
