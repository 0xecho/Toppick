# Generated by Django 3.1.14 on 2022-01-15 05:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220114_0630'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='public_url_uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
    ]