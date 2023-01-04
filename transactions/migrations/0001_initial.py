# Generated by Django 4.1.5 on 2023-01-04 21:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('cashin', 'Cashin'), ('cashout', 'Cashout')], default='cashin', max_length=8)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(max_length=256, null=True)),
                ('value', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories_transactions', to='categories.category')),
            ],
        ),
    ]
