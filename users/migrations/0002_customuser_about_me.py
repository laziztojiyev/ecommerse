# Generated by Django 5.0.1 on 2024-02-09 13:57

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='about_me',
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
