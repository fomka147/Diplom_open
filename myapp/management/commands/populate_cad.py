from django.core.management.base import BaseCommand
from myapp.models import CADSystem
from django.utils.text import slugify
from datetime import date
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Populate the database with CAD systems'

    def handle(self, *args, **kwargs):
        # Полная очистка таблицы
        CADSystem.objects.all().delete()

        cad_systems = [
            {
                'name': 'Компас-3D',
                'manufacturer': 'АСКОН',
                'category': 'mechanical',
                'description': 'Многофункциональная САПР для 3D-моделирования и 2D-черчения в машиностроении и строительстве.',
                'price': 45000.00,
                'release_date': date(2023, 1, 1),
                'image': 'cad_images/kompas-3d.png',
            },
            {
                'name': 'ЛОЦМАН:PLM',
                'manufacturer': 'АСКОН',
                'category': 'other',
                'description': 'Система управления жизненным циклом изделия, интеграция с САПР.',
                'price': 120000.00,
                'release_date': date(2022, 6, 1),
                'image': 'cad_images/lotsman-plm.png',
            },
            {
                'name': 'nanoCAD',
                'manufacturer': 'Нанософт',
                'category': 'architecture',
                'description': 'Универсальная САПР для 2D/3D-проектирования, поддержка BIM.',
                'price': 30000.00,
                'release_date': date(2024, 3, 1),
                'image': 'cad_images/nanocad.png',
            },
            {
                'name': 'SprutCAM',
                'manufacturer': 'СПРУТ-Технология',
                'category': 'cnc',
                'description': 'CAM-система для программирования ЧПУ-станков.',
                'price': 80000.00,
                'release_date': date(2023, 9, 1),
                'image': 'cad_images/sprutcam.png',
            },
            {
                'name': 'T-FLEX CAD',
                'manufacturer': 'Топ Системы',
                'category': 'mechanical',
                'description': 'Параметрическая САПР для машиностроения и промышленного дизайна.',
                'price': 60000.00,
                'release_date': date(2022, 12, 1),
                'image': 'cad_images/t-flex-cad.png',
            },
            {
                'name': 'ГЕОНОКС',
                'manufacturer': 'Нанософт',
                'category': 'architecture',
                'description': 'САПР для геодезии и землеустройства.',
                'price': 35000.00,
                'release_date': date(2023, 5, 1),
                'image': 'cad_images/placeholder.png',
            },
            {
                'name': 'Renga Architecture',
                'manufacturer': 'АСКОН',
                'category': 'architecture',
                'description': 'BIM-система для архитектурного проектирования.',
                'price': 70000.00,
                'release_date': date(2023, 7, 1),
                'image': 'cad_images/placeholder.png',
            },
            {
                'name': 'ADEM',
                'manufacturer': 'ADEM Technologies',
                'category': 'cnc',
                'description': 'CAM-система для подготовки управляющих программ ЧПУ.',
                'price': 90000.00,
                'release_date': date(2022, 10, 1),
                'image': 'cad_images/placeholder.png',
            },
            {
                'name': 'VERICUT',
                'manufacturer': 'CGTech',
                'category': 'cnc',
                'description': 'Симуляция и оптимизация ЧПУ-программ.',
                'price': 150000.00,
                'release_date': date(2024, 1, 1),
                'image': 'cad_images/placeholder.png',
            },
            {
                'name': 'КРЕДО',
                'manufacturer': 'Кредо-Диалог',
                'category': 'architecture',
                'description': 'САПР для проектирования дорог и инфраструктуры.',
                'price': 50000.00,
                'release_date': date(2023, 2, 1),
                'image': 'cad_images/placeholder.png',
            },
        ]

        for cad in cad_systems:
            # Проверяем уникальность slug
            base_slug = slugify(cad['name'])
            slug = base_slug
            counter = 1
            while CADSystem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            cad_obj = CADSystem(
                name=cad['name'],
                manufacturer=cad['manufacturer'],
                category=cad['category'],
                description=cad['description'],
                price=cad['price'],
                release_date=cad['release_date'],
                slug=slug,
            )
            if cad.get('image'):
                image_path = os.path.join('D:/Diplom_open/media/', cad['image'])
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        cad_obj.image.save(os.path.basename(image_path), File(f))
            cad_obj.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(cad_systems)} CADSystem entries'))