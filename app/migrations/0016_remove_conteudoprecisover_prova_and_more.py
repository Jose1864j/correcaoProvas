# Generated by Django 5.1.4 on 2025-01-03 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_rename_questoes_questoeserradas_questao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conteudoprecisover',
            name='prova',
        ),
        migrations.RemoveField(
            model_name='conteudorever',
            name='prova',
        ),
    ]
