# Generated by Django 2.1.8 on 2019-06-06 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.TextField(default='UNFULFILLED', max_length=250, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='product_image',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='static/staticfiles/img', verbose_name='img'),
        ),
    ]
