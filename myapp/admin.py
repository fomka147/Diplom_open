from django.contrib import admin
from .models import CADSystem, Article, Category, Feature, FAQ, Subscription, MigrationGuide


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
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


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'keywords', 'usage_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('question', 'answer', 'keywords')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'keyword', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('telegram_id', 'keyword')


@admin.register(MigrationGuide)
class MigrationGuideAdmin(admin.ModelAdmin):
    list_display = ('foreign_software', 'analogs', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('foreign_software', 'analogs', 'instruction')