# Generated by Django 3.2.2 on 2024-12-12 11:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0011_alter_patientrecord_appointment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientrecord',
            name='appointment_date',
            field=models.DateTimeField(default=datetime.date(2024, 12, 13)),
        ),
    ]
