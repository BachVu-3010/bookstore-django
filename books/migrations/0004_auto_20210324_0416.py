# Generated by Django 3.1.5 on 2021-03-24 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20210304_0313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='publiser_name',
            new_name='publisher_name',
        ),
    ]
