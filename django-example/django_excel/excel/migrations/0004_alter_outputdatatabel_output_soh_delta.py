# Generated by Django 3.2.16 on 2023-10-17 17:44

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0003_auto_20231017_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outputdatatabel',
            name='output_soh_delta',
            field=models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
        ),
    ]
