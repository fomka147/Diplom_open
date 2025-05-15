from rest_framework import serializers
from .models import CADSystem, FAQ, MigrationGuide


class CADSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CADSystem
        fields = ['name', 'developer', 'short_info', 'full_description', 'price', 'official_url', 'system_type', 'is_russian']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'keywords', 'usage_count']


class MigrationGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = MigrationGuide
        fields = ['foreign_software', 'analogs', 'instruction']