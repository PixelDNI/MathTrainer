# Generated by Django 5.0 on 2023-12-10 06:21

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminMathTrainer', '0022_answer_choice_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='paragraph',
            field=ckeditor.fields.RichTextField(),
        ),
    ]