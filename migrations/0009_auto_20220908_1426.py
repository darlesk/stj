# Generated by Django 2.2.6 on 2022-09-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stj', '0008_auto_20220908_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='tesis',
            name='nota',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='sentencia',
            name='IDSCJN',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sentencia',
            name='IDSCJN1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sentencia',
            name='no_reg',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='IUS',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='IUS1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='estado',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tesis',
            name='no_reg',
            field=models.IntegerField(),
        ),
    ]
