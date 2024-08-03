# Generated by Django 5.0.7 on 2024-08-03 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='next_available',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATE', 'CREATE'), ('CANCELLED', 'CANCELLED'), ('SENT', 'SENT'), ('DELIVERED', 'DELIVERED'), ('REJECTED', 'REJECTED'), ('NOT_COMPLETED', 'NOT_COMPLETED')], default='CREATE'),
        ),
    ]
