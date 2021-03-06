# Generated by Django 3.1.5 on 2021-03-18 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0003_auto_20210304_0313'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('payment_method', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=200)),
                ('district', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('shippingPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=5)),
                ('order', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_items', models.IntegerField()),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.book')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order')),
            ],
        ),
    ]
