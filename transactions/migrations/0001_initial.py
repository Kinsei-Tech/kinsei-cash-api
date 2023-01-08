# Generated by Django 4.1.5 on 2023-01-08 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('cashin', 'Cashin'), ('cashout', 'Cashout')], default='cashin', max_length=8)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=256, null=True)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=1000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories_transactions', to='categories.category')),
            ],
        ),
    ]
