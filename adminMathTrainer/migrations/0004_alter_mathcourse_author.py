# Generated by Django 4.2.4 on 2023-12-03 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminMathTrainer', '0003_mathcourse_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mathcourse',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
