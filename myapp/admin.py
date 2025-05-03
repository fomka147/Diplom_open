from django.contrib import admin
from .models import CADSystem, Article, Category, Feature

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(CADSystem)
class CADSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'developer', 'category', 'price', 'rating', 'is_russian', 'is_active', 'is_featured')
    list_filter = ('category', 'developer', 'is_russian', 'is_active', 'is_featured', 'system_type', 'license_type')
    search_fields = ('name', 'developer', 'short_info', 'full_description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('features',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'slug')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}