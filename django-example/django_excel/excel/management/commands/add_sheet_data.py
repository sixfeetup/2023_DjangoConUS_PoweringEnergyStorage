import json
import pandas as pd
from decimal import Decimal as D
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder

from excel.models import ConstantData


class Command(BaseCommand):

    def convert_data_to_df(self, file, columns, skiprows):
        """
        Read and excel file with specific columns and skip any non required 
        rows you encounter during reading rows.
        """
        specifications = pd.read_excel(file, skiprows=skiprows, usecols=columns)
        return specifications

    def convert_data_type(self, data_property):
        """
        Convert pandas series to list of data.
        """
        return json.dumps(data_property.tolist())

    def get_constant_data_for_project(self, sheet_name, columns, skiprows, total_rows):
        """
        Read only specific columns from the excel file.
        """
        data = self.convert_data_to_df(sheet_name, columns=columns, skiprows=skiprows).iloc[0:total_rows]
        return data

    def handle(self, *args, **kwargs):
        sheet_name = "./excel/data/sample.xlsx"
        # Read columns data
        columns = "T:X"
        skiprows = 54
        total_rows = 40

        sheet_data = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)

        PERFORMANCE_DETERIORATION_PROFILE =  self.convert_data_type(sheet_data["Performance Deterioration Profile"])
        STEPWISE_DIRECT_CURRENT_GENERATION_INCREASE = self.convert_data_type(sheet_data["Stepwise Direct Current Generation Increase"])
        DETERIORATION_CURVE_FOR_PHASE_GREATER_THAN1 = self.convert_data_type(sheet_data["Deterioration Curve for Phase Greater Than 1"])
        PROGRESSIVE_PROJECT_DIRECT_CURRENT_GENERATION = self.convert_data_type(sheet_data["Progressive Project Direct Current Generation"])
        PERFORMANCE_DECAY_WITH_PERFORMANCE_GRID_MATRIX = self.convert_data_type(sheet_data["Performance Decay with Performance Grid Matrix"])
        # Read Input Columns Data
        columns = "T:V"
        skiprows = 95
        total_rows = 40

        input_columns_data_array = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)
        initial_energy = self.convert_data_type(input_columns_data_array["Initial Energy (MWh)"])
        phase1_data = self.convert_data_type(input_columns_data_array["Phase 1 Data"])
        phase2_data = self.convert_data_type(input_columns_data_array["Phase 2 Data"])

        # Read Constant Data
        columns = "P:Q"
        skiprows = 57
        total_rows = 6

        constant_data = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)
        annual_operating_cycles = constant_data.iloc[0, 1]
        duration_of_project = constant_data.iloc[1, 1]
        steady_output = True if constant_data.iloc[2, 1]=="Yes" else False 
        electrical_capacity = constant_data.iloc[3, 1]
        minimum_capacity = constant_data.iloc[4, 1]
        losses = constant_data.iloc[5, 1]

        # Read Output Data
        columns = "M"
        skiprows = 50
        total_rows = 40
        output_data_array = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)
        output_data = self.convert_data_type(output_data_array["Performance Decay with Performance Grid Matrix vs. Initial State of Health (ISOH) Delta"])

        ConstantData.objects.create(
            annual_operating_cycles=annual_operating_cycles,
            duration_of_project=duration_of_project,
            steady_output=steady_output,
            electrical_capacity=electrical_capacity,
            minimum_capacity=minimum_capacity,
            losses=losses,
            performance_deterioration_profile=PERFORMANCE_DETERIORATION_PROFILE,
            stepwise_direct_current_generation_increase=STEPWISE_DIRECT_CURRENT_GENERATION_INCREASE,
            deterioration_curve_for_phase_greater_than1=DETERIORATION_CURVE_FOR_PHASE_GREATER_THAN1,
            progressive_project_direct_current_generation=PROGRESSIVE_PROJECT_DIRECT_CURRENT_GENERATION,
            performance_decay_with_performance_grid_matrix=PERFORMANCE_DECAY_WITH_PERFORMANCE_GRID_MATRIX,
            initial_energy=initial_energy,
            phase1_data=phase1_data,
            phase2_data=phase2_data,
            result=output_data,
        )
        return "True"