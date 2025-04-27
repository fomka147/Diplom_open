from django.core.management.base import BaseCommand
from myapp.models import CADSystem
from datetime import date
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate CADSystem database'

    def handle(self, *args, **kwargs):
        CADSystem.objects.all().delete()
        systems = [
            {'name': 'Компас-3D', 'manufacturer': 'АСКОН', 'category': 'mechanical', 'description': 'Российская САПР для 3D-моделирования и чертежей по ЕСКД.', 'price': Decimal('150000.00'), 'release_date': date(2023, 1, 1), 'slug': 'kompas-3d'},
            {'name': 'NanoCAD', 'manufacturer': 'NanoSoft', 'category': 'architecture', 'description': 'Доступная САПР для 2D/3D-проектирования в архитектуре.', 'price': Decimal('45000.00'), 'release_date': date(2022, 6, 1), 'slug': 'nanocad'},
            {'name': 'T-FLEX CAD', 'manufacturer': 'Топ Системы', 'category': 'mechanical', 'description': 'Параметрическое проектирование для машиностроения.', 'price': Decimal('200000.00'), 'release_date': date(2021, 3, 15), 'slug': 't-flex-cad'},
            {'name': 'Renga Architecture', 'manufacturer': 'Renga Software', 'category': 'architecture', 'description': 'BIM-моделирование для архитектурного проектирования.', 'price': Decimal('80000.00'), 'release_date': date(2022, 9, 1), 'slug': 'renga-architecture'},
            {'name': 'СПРУТ-ТП', 'manufacturer': 'Sprut Technology', 'category': 'cnc', 'description': 'Подготовка программ для станков с ЧПУ.', 'price': Decimal('120000.00'), 'release_date': date(2020, 11, 1), 'slug': 'sprut-tp'},
            {'name': 'ADEM', 'manufacturer': 'ADEM Technologies', 'category': 'cnc', 'description': 'САПР для технологической подготовки производства.', 'price': Decimal('100000.00'), 'release_date': date(2019, 5, 1), 'slug': 'adem'},
            {'name': 'K3-Мебель', 'manufacturer': 'К3', 'category': 'other', 'description': 'САПР для проектирования мебели и интерьеров.', 'price': Decimal('90000.00'), 'release_date': date(2021, 7, 1), 'slug': 'k3-mebel'},
            {'name': 'Лира-САПР', 'manufacturer': 'Лира софт', 'category': 'architecture', 'description': 'Расчет строительных конструкций и BIM-интеграция.', 'price': Decimal('130000.00'), 'release_date': date(2020, 2, 1), 'slug': 'lira-sapr'},
            {'name': 'Autodesk Inventor', 'manufacturer': 'Autodesk', 'category': 'mechanical', 'description': '3D-моделирование для машиностроения.', 'price': Decimal('250000.00'), 'release_date': date(2023, 4, 1), 'slug': 'autodesk-inventor'},
            {'name': 'SolidWorks', 'manufacturer': 'Dassault Systèmes', 'category': 'mechanical', 'description': 'САПР для проектирования в машиностроении.', 'price': Decimal('300000.00'), 'release_date': date(2022, 10, 1), 'slug': 'solidworks'},
            {'name': 'AutoCAD', 'manufacturer': 'Autodesk', 'category': 'architecture', 'description': 'Лидер в 2D/3D-проектировании.', 'price': Decimal('200000.00'), 'release_date': date(2023, 3, 1), 'slug': 'autocad'},
            {'name': 'Creo', 'manufacturer': 'PTC', 'category': 'mechanical', 'description': 'САПР для параметрического моделирования.', 'price': Decimal('280000.00'), 'release_date': date(2022, 5, 1), 'slug': 'creo'},
            {'name': 'NX', 'manufacturer': 'Siemens', 'category': 'mechanical', 'description': 'Интегрированная САПР для сложных проектов.', 'price': Decimal('350000.00'), 'release_date': date(2021, 9, 1), 'slug': 'nx'},
            {'name': 'CATIA', 'manufacturer': 'Dassault Systèmes', 'category': 'mechanical', 'description': 'САПР для авиации и автомобилестроения.', 'price': Decimal('400000.00'), 'release_date': date(2022, 7, 1), 'slug': 'catia'},
            {'name': 'BricsCAD', 'manufacturer': 'Bricsys', 'category': 'architecture', 'description': 'Альтернатива AutoCAD для 2D/3D.', 'price': Decimal('60000.00'), 'release_date': date(2023, 2, 1), 'slug': 'bricscad'},
            {'name': 'ZWCAD', 'manufacturer': 'ZWSOFT', 'category': 'architecture', 'description': 'Экономичная САПР для архитектуры.', 'price': Decimal('50000.00'), 'release_date': date(2022, 11, 1), 'slug': 'zwcad'},
            {'name': 'SCAD Office', 'manufacturer': 'SCAD Soft', 'category': 'architecture', 'description': 'Расчет конструкций для строительства.', 'price': Decimal('110000.00'), 'release_date': date(2020, 4, 1), 'slug': 'scad-office'},
            {'name': 'Tekla Structures', 'manufacturer': 'Trimble', 'category': 'architecture', 'description': 'BIM для стальных конструкций.', 'price': Decimal('250000.00'), 'release_date': date(2023, 6, 1), 'slug': 'tekla-structures'},
            {'name': 'Advance Steel', 'manufacturer': 'Autodesk', 'category': 'architecture', 'description': 'САПР для стальных конструкций.', 'price': Decimal('180000.00'), 'release_date': date(2022, 8, 1), 'slug': 'advance-steel'},
            {'name': 'Topomatic Robur', 'manufacturer': 'Topomatic', 'category': 'other', 'description': 'САПР для проектирования дорог.', 'price': Decimal('140000.00'), 'release_date': date(2021, 1, 1), 'slug': 'topomatic-robur'},
        ]
        for system in systems:
            CADSystem.objects.create(**system)
        self.stdout.write(self.style.SUCCESS('Successfully populated 20 CADSystem entries'))