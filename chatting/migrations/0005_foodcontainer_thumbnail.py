# Generated by Django 4.2.7 on 2023-11-26 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0004_alter_foodcontainer_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodcontainer',
            name='thumbnail',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]