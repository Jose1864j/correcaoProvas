# Generated by Django 5.1.4 on 2025-03-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaQuestoes', '0006_questoesassinalar_gabaritolancado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questoesassinalar',
            name='gabaritoLancado',
        ),
        migrations.AddField(
            model_name='listas',
            name='gabaritoLancado',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
