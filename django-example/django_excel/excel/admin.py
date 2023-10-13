from django.contrib import admin, messages
from django.core import management
from django.db.models import JSONField
from django.http import HttpResponseRedirect
from django.urls import path

from django_json_widget.widgets import JSONEditorWidget

from excel.models import ConstantData, OutputDataTabel


@admin.register(ConstantData)
class ConstantDataAdmin(admin.ModelAdmin):
    list_display = ["__str__" ,"project_cycles_per_year", "project_term", "constant_throughput", "project_ecap", "project_min_e_capacity", "project_e_losses"]
    list_filter = ["project_cycles_per_year", "project_term"]
    actions = ["generate_results"]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

    change_list_template = "admin/data_change_list.html"

    def generate_results(modeladmin, request, queryset):
        OutputDataTabel.generate_output(queryset)

    def ingest_constant_data(self, request):
        success = management.call_command("add_sheet_data")
        if success:
            messages.add_message(
                request,
                messages.SUCCESS,
                "Successfully Ingested Data",
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Error occurred while ingesting data",
            )
        return HttpResponseRedirect("../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "ingest_constant_data/",
                self.ingest_constant_data,
                name="ingest_constant_data",
            ),
        ]
        return custom_urls + urls
    

@admin.register(OutputDataTabel)
class OutputDataTabelAdmin(admin.ModelAdmin):
    list_display = ["__str__"]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
