# Generated by Django 4.1.5 on 2023-01-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_is_healthy"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="current_balance",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=1000),
        ),
        migrations.AlterField(
            model_name="user",
            name="goal_balance",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=1000, null=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="total_balance",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=1000, null=True
            ),
        ),
    ]