from django.contrib import admin
from .models import CADSystem

@admin.register(CADSystem)
class CADSystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'category', 'price', 'release_date']
    list_filter = ['category', 'manufacturer']
    search_fields = ['name', 'description']