# Generated by Django 5.0.2 on 2024-03-16 19:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("apartments", "0003_delete_visit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="apartment",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
    ]
