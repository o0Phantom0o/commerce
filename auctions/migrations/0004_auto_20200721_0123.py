# Generated by Django 3.0.8 on 2020-07-20 20:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20200721_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='picture',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='title',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
    ]
