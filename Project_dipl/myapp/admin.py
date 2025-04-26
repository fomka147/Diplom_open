from django.contrib import admin
from .models import Category, CADSystem, Feature

class FeatureInline(admin.TabularInline):
    model = CADSystem.features.through
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order', 'color')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'color')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CADSystem)
class CADSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'is_featured', 'price', 'is_russian')
    list_editable = ('is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured', 'is_russian', 'system_type')
    search_fields = ('name', 'developer', 'short_info')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('features',)
    inlines = [FeatureInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'developer', 'category', 'short_info', 'full_description')
        }),
        ('Изображения', {
            'fields': ('image', 'screenshot')
        }),
        ('Цена и лицензия', {
            'fields': ('price', 'license_type', 'is_russian')
        }),
        ('Технические детали', {
            'fields': ('system_type', 'platforms', 'file_formats')
        }),
        ('Характеристики и оценки', {
            'fields': ('features', 'advantages', 'disadvantages', 'rating')
        }),
        ('Ссылки', {
            'fields': ('official_url', 'demo_url', 'docs_url')
        }),
        ('Метаданные', {
            'fields': ('is_active', 'is_featured', 'slug')
        }),
    )

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)