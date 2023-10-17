import json
from decimal import Decimal as D
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder


def convert_to_dict(data_str):
    data = json.loads(data_str)
    return {int(index): D(value) for index, value in enumerate(data, start=1)}


class ConstantData(models.Model):
    # Constants
    annual_operating_cycles = models.IntegerField(null=True, blank=True)
    duration_of_project = models.IntegerField(null=True, blank=True)
    steady_output = models.BooleanField(null=True, blank=True)
    electrical_capacity = models.IntegerField(null=True, blank=True)
    minimum_capacity = models.IntegerField(null=True, blank=True)
    losses = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9)

    # Column Constant Values
    performance_deterioration_profile = models.JSONField(default=list, null=True, blank=True)
    stepwise_direct_current_generation_increase = models.JSONField(default=list, null=True, blank=True)
    deterioration_curve_for_phase_greater_than1 = models.JSONField(default=list, null=True, blank=True)
    progressive_project_direct_current_generation = models.JSONField(default=list, null=True, blank=True)
    performance_decay_with_performance_grid_matrix = models.JSONField(default=list, null=True, blank=True)

    # Other Sheets Data
    initial_energy = models.JSONField(default=list, null=True, blank=True)
    phase1_data = models.JSONField(default=list, null=True, blank=True)
    phase2_data = models.JSONField(default=list, null=True, blank=True)

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
            performance_table = PerformanceTableProject(
                performance_decay_with_performance_grid_matrix=convert_to_dict(constant_data.performance_decay_with_performance_grid_matrix),
                progressive_project_direct_current_generation=convert_to_dict(constant_data.progressive_project_direct_current_generation),
                performance_deterioration_profile=convert_to_dict(constant_data.performance_deterioration_profile),
                deterioration_curve_for_phase_greater_than1=convert_to_dict(constant_data.deterioration_curve_for_phase_greater_than1),
            )
            performance_table.initialize_phases()

            OutputDataTabel.objects.create(
                data=constant_data,
                output_soh_delta=json.dumps(performance_table.project_performance_decay_with_performance_grid_matrix_delta, cls=DjangoJSONEncoder)
            )

class Phase:
    """Calculate Performance Table Phase formulas for the project."""

    def __init__(
            self, 
            pg_table_project,
            phase_info,
        ):
        """Constructor"""
        self.phase_info = phase_info
        self.years = [year for year in range(1, 41)]
        self.pg_table_project = pg_table_project


    @property
    def incremental_phase_dc_generation(self):
        """
        Incremental Phase DC  Generation (MWhDC Out)
        """
        return self.incremental_phase_dc_generation

    @property
    def total_phase_dc_generation(self):
        """
        Total Phase Dc Generation (MWhDC Out)
        =SUM(Hn:H$n)
        """
        # n is a natural number
        incremental_phase_dc_generation = self.incremental_phase_dc_generation
        result = {1: 0, 2: incremental_phase_dc_generation[2]}
        for year in self.years[2:]:
            result[year] = sum(
                [incremental_phase_dc_generation[prev_year] for prev_year in result]
                + [incremental_phase_dc_generation[year]]
            )
        return result

    @property
    def phase_years(self):
        """
        Total Years for a project
        """
        return self.years

    @property
    def performance_decay_with_performance_grid_matrix(self):
        """
        A constant value throughout the project
        """
        return self.pg_table_project.performance_decay_with_performance_grid_matrix

    @property
    def performance_decay_with_performance_grid_matrix_delta(self):
        """
        Performance Decay With Performance Grid Matrix Delta
        """
        phase_degradation_with_deterioration_profile = (
            self.pg_table_project.performance_deterioration_profile
            if self.phase_info == 1
            else self.pg_table_project.deterioration_curve_for_phase_greater_than1
        )
        performance_decay_with_performance_grid_matrix = self.pg_table_project.performance_decay_with_performance_grid_matrix
        result = {}
        for year in self.years:
            result[year] = abs(
                performance_decay_with_performance_grid_matrix[year]
                - D(phase_degradation_with_deterioration_profile[year])
            )
        return result
    

class PerformanceTableProject:
    """Performance Table formulas"""

    phase_1 = None
    phase_2 = None

    def __init__(
            self, 
            performance_decay_with_performance_grid_matrix, 
            progressive_project_direct_current_generation,
            performance_deterioration_profile,
            deterioration_curve_for_phase_greater_than1,
        ):
        self.years = [year for year in range(1, 41)]
        self.performance_decay_with_performance_grid_matrix = performance_decay_with_performance_grid_matrix
        self.progressive_project_direct_current_generation = progressive_project_direct_current_generation
        self.performance_deterioration_profile = performance_deterioration_profile
        self.deterioration_curve_for_phase_greater_than1 = deterioration_curve_for_phase_greater_than1

    def initialize_phases(self):
        for phase in [phase for phase in range(1, 3)]:
            setattr(
                self, 
                f"phase_{phase}", 
                Phase(
                    phase_info=phase,
                    pg_table_project=self
                ),
            )

    @property
    def project_performance_decay_with_performance_grid_matrix_delta(self):
        """Project Performance Decay With Performance Grid Matrix Delta"""
        phase_deg_pg_matrix = {}
        for phase in [phase for phase in range(1, 3)]:
            phase_obj = getattr(self, f"phase_{phase}")
            phase_deg_pg_matrix[phase] = phase_obj.performance_decay_with_performance_grid_matrix_delta

        result = {}
        for year in self.years:
            result[year] = max(
                [phase_deg_pg_matrix[phase][year] for phase in [phase for phase in range(1, 3)]]
            )

        return result

    @property
    def project_cycles(self):
        result = {1: 0}
        for year in self.years[1:]:
            result[year] = result[year - 1] + self.cycles_per_year
        return result

