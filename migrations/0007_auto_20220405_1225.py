# Generated by Django 2.2.6 on 2022-04-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stj', '0006_auto_20220405_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tesis',
            name='precedente',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='referencia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='rubro',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='sala_pleno',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='texto',
            field=models.TextField(blank=True, null=True),
        ),
    ]