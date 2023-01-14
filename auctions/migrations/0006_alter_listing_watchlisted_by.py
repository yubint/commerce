# Generated by Django 4.1.5 on 2023-01-14 12:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_comment_user_alter_listing_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlisted_by',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
