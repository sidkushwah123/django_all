from django.contrib import admin
from .models import AwColor
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class AwColorAdmin(ImportExportModelAdmin):
    list_display = ('Color_name','Slug','Status' ,'Created_by','Created_date','Updated_date')
    list_filter = ('Created_date','Updated_date',)
    

admin.site.register(AwColor,AwColorAdmin)
