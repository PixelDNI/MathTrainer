# Generated by Django 4.2.4 on 2023-12-09 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminMathTrainer', '0016_alter_coursemodule_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lecture',
            old_name='course_module',
            new_name='module',
        ),
    ]