# Generated by Django 4.1.7 on 2023-03-09 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id_product', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('site', models.TextField(max_length=500)),
                ('quote_date', models.DateField()),
                ('link_image', models.TextField(default='https://via.placeholder.com/150', max_length=500)),
            ],
        ),
    ]
