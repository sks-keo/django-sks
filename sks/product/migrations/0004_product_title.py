# Generated by Django 2.0.6 on 2018-06-20 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20180620_0635'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(db_index=True, default='no-title', max_length=256, verbose_name='title'),
        ),
    ]
