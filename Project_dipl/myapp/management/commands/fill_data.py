from django.core.management.base import BaseCommand
from myapp.models import Category, CADSystem


class Command(BaseCommand):
    help = "Fill database with test data"

    def handle(self, *args, **options):
        # Создаём категорию
        category = Category.objects.create(
            name="Строительство",
            description="САПР для строительных компаний"
        )

        # Создаём САПР-систему
        CADSystem.objects.create(
            category=category,
            name="AutoCAD",
            short_info="Лидер рынка САПР",
            price=150000,
            official_url="https://autodesk.ru"
        )
        self.stdout.write("Данные добавлены!")