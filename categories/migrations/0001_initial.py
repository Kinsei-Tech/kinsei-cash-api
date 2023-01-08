# Generated by Django 4.1.5 on 2023-01-08 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('house bills', 'House Bills'), ('leisure', 'Leisure'), ('education', 'Education'), ('investment', 'Investment'), ('health', 'Health'), ('travel', 'Travel'), ('self_care', 'Self Care'), ('clothes', 'Clothes'), ('gifts', 'Gifts'), ('transportation', 'Transportation'), ('food', 'Food'), ('donation', 'Donation'), ('other', 'Other')], default='other', max_length=20)),
                ('limit', models.DecimalField(decimal_places=2, default=0, max_digits=1000)),
            ],
        ),
    ]
