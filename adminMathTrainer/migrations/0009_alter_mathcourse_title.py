# Generated by Django 4.2.4 on 2023-12-03 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminMathTrainer', '0008_alter_mathcourse_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mathcourse',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
