# Generated by Django 3.0.8 on 2020-07-25 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20200724_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='watch',
            name='bidId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.bid'),
            preserve_default=False,
        ),
    ]
