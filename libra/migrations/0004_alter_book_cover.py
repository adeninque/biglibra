# Generated by Django 4.1.7 on 2023-04-08 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libra', '0003_book_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(upload_to='book-cover/%y/%m/%d'),
        ),
    ]