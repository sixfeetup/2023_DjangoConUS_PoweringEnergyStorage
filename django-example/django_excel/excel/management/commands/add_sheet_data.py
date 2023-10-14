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
        Convert list of data into a dictionary, where keys
        represent the years and values represent the values
        against that year. 
        """
        output = {
            index: value
                for index, value in enumerate(data_property, start=1)
        }
        return json.dumps(output)

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
        DEGRADATION_CURVE =  self.convert_data_type(sheet_data["DEGRADATION_CURVE"])
        INCREMENTAL_TRANCHE_DC_OUTPUT = self.convert_data_type(sheet_data["INCREMENTAL_TRANCHE_DC_OUTPUT"])
        DEGRADATION_CURVE_TRANCHE_GT_1 = self.convert_data_type(sheet_data["DEGRADATION_CURVE_TRANCHE_GT_1"])
        INCREMENTAL_PROJECT_DC_OUTPUT = self.convert_data_type(sheet_data["INCREMENTAL_PROJECT_DC_OUTPUT"])
        DEGRADATION_WITH_PG_MATRIX = self.convert_data_type(sheet_data["DEGRADATION_WITH_PG_MATRIX"])

        # Read Input Columns Data
        columns = "T:v"
        skiprows = 95
        total_rows = 40

        input_columns_data_array = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)
        energy_capacity_before_losses = self.convert_data_type(input_columns_data_array["Energy Capacity before Losses (MWh)"])
        tranche1_data = self.convert_data_type(input_columns_data_array["Tranche 1 Data"])
        tranche2_data = self.convert_data_type(input_columns_data_array["Tranche 2 Data"])

        # Read Constant Data
        columns = "P:Q"
        skiprows = 57
        total_rows = 6

        constant_data = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)
        project_cycles_per_year = constant_data.iloc[0, 1]
        project_term = constant_data.iloc[1, 1]
        constant_throughput = True if constant_data.iloc[2, 1]=="Yes" else False 
        project_ecap = constant_data.iloc[3, 1]
        project_min_e_capacity = constant_data.iloc[4, 1]
        project_e_losses = constant_data.iloc[5, 1]

        # Read Output Data
        columns = "M"
        skiprows = 50
        total_rows = 40
        output_data_array = self.get_constant_data_for_project(sheet_name, columns, skiprows, total_rows)
        output_data = self.convert_data_type(output_data_array["Deg w/ PG Matrix vs HARD INPUT SOH Delta"])

        ConstantData.objects.create(
            project_cycles_per_year=project_cycles_per_year,
            project_term=project_term,
            constant_throughput=constant_throughput,
            project_ecap=project_ecap,
            project_min_e_capacity=project_min_e_capacity,
            project_e_losses=project_e_losses,
            degradation_curve=DEGRADATION_CURVE,
            incremental_tranche_dc_output=INCREMENTAL_TRANCHE_DC_OUTPUT,
            degradation_curve_tranche_gt_1=DEGRADATION_CURVE_TRANCHE_GT_1,
            incremental_project_dc_output=INCREMENTAL_PROJECT_DC_OUTPUT,
            degradation_with_pg_matrix=DEGRADATION_WITH_PG_MATRIX,
            energy_capacity_before_losses=energy_capacity_before_losses,
            tranche1_data=tranche1_data,
            tranche2_data=tranche2_data,
            result=output_data,
        )
        return "True"