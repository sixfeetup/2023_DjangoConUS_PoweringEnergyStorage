import json
from decimal import Decimal as D
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


def convert_to_dict(data_str):
    data = json.loads(data_str)
    return {int(key): D(value) for key, value in data.items()}


class ConstantData(models.Model):
    # Constants
    project_cycles_per_year = models.IntegerField(null=True, blank=True)
    project_term = models.IntegerField(null=True, blank=True)
    constant_throughput = models.BooleanField(null=True, blank=True)
    project_ecap = models.IntegerField(null=True, blank=True)
    project_min_e_capacity = models.IntegerField(null=True, blank=True)
    project_e_losses = models.IntegerField(null=True, blank=True)

    # Column Constant Values
    degradation_curve = models.JSONField(default=dict, null=True, blank=True)
    incremental_tranche_dc_output = models.JSONField(default=dict, null=True, blank=True)
    degradation_curve_tranche_gt_1 = models.JSONField(default=dict, null=True, blank=True)
    incremental_project_dc_output = models.JSONField(default=dict, null=True, blank=True)
    degradation_with_pg_matrix = models.JSONField(default=dict, null=True, blank=True)

    # Other Sheets Data
    energy_capacity_before_losses = models.JSONField(default=list, null=True, blank=True)
    tranche1_data = models.JSONField(default=list, null=True, blank=True)
    tranche2_data = models.JSONField(default=list, null=True, blank=True)

    # Result
    result = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return f"Constant Data for project : {self.id}"


class OutputDataTabel(models.Model):
    data = models.ForeignKey(ConstantData, on_delete=models.CASCADE)
    output_soh_delta = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"Output for data id: {self.data.id}"

    @classmethod
    def generate_output(cls, queryset):
        for constant_data in queryset:
            pg_table = PgTableProject(
                degradation_with_pg_matrix=convert_to_dict(constant_data.degradation_with_pg_matrix),
                incremental_tranche_dc_output=convert_to_dict(constant_data.incremental_tranche_dc_output),
                degradation_curve=convert_to_dict(constant_data.degradation_curve),
                degradation_curve_tranche_gt_1=convert_to_dict(constant_data.degradation_curve_tranche_gt_1),
            )
            pg_table.initialize_tranches()

            OutputDataTabel.objects.create(
                data=constant_data,
                output_soh_delta=json.dumps(pg_table.project_pg_matrix_hard_input_soh_delta, cls=DjangoJSONEncoder)
            )

class Tranche:
    """Calculate PG Table Tranche formulas for the project."""

    def __init__(
            self, 
            pg_table_project,
            tranche_info,
        ):
        """Constructor"""
        self.tranche_info = tranche_info
        self.years = [year for year in range(1, 41)]
        self.pg_table_project = pg_table_project


    @property
    def incremental_tranche_dc_output(self):
        """
        Incremental Tranche DC  Output (MWhDC Out)
        =IF(E98<2, 0, IFERROR(I53*(Augmentation!L10/Augmentation!$J10),0))
        """
        return self.incremental_tranche_dc_output

    @property
    def aggregate_tranche_dc_output(self):
        """
        Aggregate Tranche DC  Output (MWhDC Out)
        =SUM(Hn:H$n)
        """
        # n is a natural number
        incremental_tranche_dc_output = self.incremental_tranche_dc_output
        result = {1: 0, 2: incremental_tranche_dc_output[2]}
        for year in self.years[2:]:
            result[year] = sum(
                [incremental_tranche_dc_output[prev_year] for prev_year in result]
                + [incremental_tranche_dc_output[year]]
            )
        return result

    @property
    def tranche_years(self):
        """
        Total Years for a project
        """
        return self.years

    @property
    def degradation_with_pg_matrix(self):
        """
        A constant value throughout the project
        """
        return self.pg_table_project.degradation_with_pg_matrix

    @property
    def pg_matrix_hard_input_soh_delta(self):
        """
        Deg w/ PG Matrix vs HARD INPUT SOH Delta
        """
        tranche_degradation_with_pg_matrix_prev = (
            self.pg_table_project.degradation_curve
            if self.tranche_info == 1
            else self.pg_table_project.degradation_curve_tranche_gt_1
        )
        degradation_with_pg_matrix = self.pg_table_project.degradation_with_pg_matrix
        result = {}
        for year in self.years:
            result[year] = abs(
                round(degradation_with_pg_matrix[year], 6)
                - round(D(tranche_degradation_with_pg_matrix_prev[year]), 6)
            )
        return result
    

class PgTableProject:
    """PG sheet project table formulas"""

    tranche_1 = None
    tranche_2 = None

    def __init__(
            self, 
            degradation_with_pg_matrix, 
            incremental_tranche_dc_output,
            degradation_curve,
            degradation_curve_tranche_gt_1,
        ):
        self.years = [year for year in range(1, 41)]
        self.degradation_with_pg_matrix = degradation_with_pg_matrix
        self.incremental_tranche_dc_output = incremental_tranche_dc_output
        self.degradation_curve = degradation_curve
        self.degradation_curve_tranche_gt_1 = degradation_curve_tranche_gt_1

    def initialize_tranches(self):
        for tranche in [tranche for tranche in range(1, 3)]:
            setattr(
                self, 
                f"tranche_{tranche}", 
                Tranche(
                    tranche_info=tranche,
                    pg_table_project=self
                ),
            )

    @property
    def project_pg_matrix_hard_input_soh_delta(self):
        """Calculate Deg w/ PG Matrix vs HARD INPUT SOH Delta"""
        tranche_deg_pg_matrix = {}
        for tranche in [tranche for tranche in range(1, 3)]:
            tranche_obj = getattr(self, f"tranche_{tranche}")
            tranche_deg_pg_matrix[tranche] = tranche_obj.pg_matrix_hard_input_soh_delta

        result = {}
        for year in self.years:
            result[year] = max(
                [tranche_deg_pg_matrix[tranche][year] for tranche in [tranche for tranche in range(1, 3)]]
            )

        return result

    @property
    def project_cycles(self):
        result = {1: 0}
        for year in self.years[1:]:
            result[year] = result[year - 1] + self.cycles_per_year
        return result

