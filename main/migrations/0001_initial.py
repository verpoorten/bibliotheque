# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auteur',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecteur',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Livre',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('langue', models.CharField(choices=[('FR', 'Français'), ('ENG', 'Anglais')], max_length=5, default='FR')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date_debut_location', models.DateField()),
                ('date_fin_location', models.DateField(blank=True, null=True)),
                ('remarque', models.TextField(blank=True, null=True)),
                ('lecteur', models.ForeignKey(to='main.Lecteur')),
                ('livre', models.ForeignKey(to='main.Livre')),
            ],
        ),
        migrations.CreateModel(
            name='Proprietaire',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('livre', models.ForeignKey(to='main.Livre')),
                ('proprietaire', models.ForeignKey(to='main.Lecteur')),
            ],
        ),
    ]
