# Generated by Django 4.1.6 on 2023-02-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoping_for_himself', '0004_remove_modeltitle_title_remove_offer_model_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
