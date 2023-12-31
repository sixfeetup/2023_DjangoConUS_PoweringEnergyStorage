# Generated by Django 3.2.16 on 2023-10-17 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0002_auto_20231017_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constantdata',
            name='deterioration_curve_for_phase_greater_than1',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='constantdata',
            name='performance_decay_with_performance_grid_matrix',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='constantdata',
            name='performance_deterioration_profile',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='constantdata',
            name='progressive_project_direct_current_generation',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='constantdata',
            name='stepwise_direct_current_generation_increase',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
