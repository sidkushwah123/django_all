# Generated by Django 3.0.6 on 2020-10-15 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_manage_setting', '0005_auto_20201015_0645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='awmanageshipping',
            old_name='min_ordr_amount_amount',
            new_name='min_ordr_amount',
        ),
    ]