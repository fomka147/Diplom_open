from django.db import models


class Feature(models.Model):
    """Модель для характеристик системы"""
    name = models.CharField("Характеристика", max_length=200, unique=True)
    icon = models.CharField("Иконка", max_length=50, blank=True,
                            help_text="Иконка из Bootstrap Icons (например, 'bi-check')")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий систем"""
    COLOR_CHOICES = [
        ('primary', 'Синий (primary)'),
        ('secondary', 'Серый (secondary)'),
        ('success', 'Зеленый (success)'),
        ('danger', 'Красный (danger)'),
        ('warning', 'Желтый (warning)'),
        ('info', 'Голубой (info)'),
        ('dark', 'Темный (dark)'),
    ]

    name = models.CharField("Название", max_length=100, unique=True)
    description = models.TextField("Описание")
    icon = models.CharField("Иконка", max_length=50, default="bi-pc-display",
                            help_text="Иконка из Bootstrap Icons (например, 'bi-gear')")
    color = models.CharField("Цвет", max_length=20, choices=COLOR_CHOICES,
                             default='primary')
    slug = models.SlugField("URL-адрес", max_length=100, unique=True,
                            help_text="ЧПУ для URL (например, 'graphic-cad')")
    order = models.PositiveIntegerField("Порядок отображения", default=0)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class CADSystem(models.Model):
    """Модель систем автоматизированного проектирования"""
    TYPE_CHOICES = [
        ('CAD', 'Система проектирования'),
        ('CAM', 'Система производства'),
        ('CAE', 'Инженерный анализ'),
        ('BIM', 'Информационное моделирование зданий'),
        ('PLM', 'Управление жизненным циклом'),
    ]

    LICENSE_CHOICES = [
        ('permanent', 'Постоянная лицензия'),
        ('subscription', 'Подписка'),
        ('free', 'Бесплатная'),
        ('trial', 'Пробная версия'),
    ]

    # Основная информация
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='systems',
        verbose_name="Категория"
    )
    name = models.CharField("Название", max_length=100)
    developer = models.CharField("Разработчик", max_length=100)
    short_info = models.TextField("Краткое описание")
    full_description = models.TextField("Полное описание", blank=True)

    # Изображения
    image = models.ImageField(
        "Логотип",
        upload_to='sapr_images/',
        blank=True,
        help_text="Рекомендуемый размер: 300x300px"
    )
    screenshot = models.ImageField(
        "Скриншот интерфейса",
        upload_to='sapr_screenshots/',
        blank=True,
        null=True
    )

    # Цена и лицензия
    price = models.DecimalField(
        "Цена",
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )
    license_type = models.CharField(
        "Тип лицензии",
        max_length=12,
        choices=LICENSE_CHOICES,
        default='subscription'
    )
    is_russian = models.BooleanField("Российское ПО", default=False)

    # Технические детали
    system_type = models.CharField(
        "Тип системы",
        max_length=3,
        choices=TYPE_CHOICES,
        default='CAD'
    )
    platforms = models.CharField(
        "Платформы",
        max_length=100,
        blank=True,
        help_text="Например: Windows, Linux, macOS"
    )
    file_formats = models.CharField(
        "Поддерживаемые форматы",
        max_length=200,
        blank=True
    )

    # Характеристики и оценки
    features = models.ManyToManyField(
        Feature,
        verbose_name="Характеристики",
        blank=True
    )
    advantages = models.TextField("Преимущества", blank=True)
    disadvantages = models.TextField("Недостатки", blank=True)
    rating = models.FloatField(
        "Рейтинг",
        default=0.0,
        help_text="От 0 до 5"
    )

    # Ссылки
    official_url = models.URLField("Официальный сайт")
    demo_url = models.URLField(
        "Ссылка на демо-версию",
        blank=True
    )
    docs_url = models.URLField(
        "Ссылка на документацию",
        blank=True
    )

    # Метаданные
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_active = models.BooleanField("Активна", default=True)
    is_featured = models.BooleanField("Рекомендуемая", default=False)
    slug = models.SlugField("URL", max_length=100, unique=True)

    class Meta:
        verbose_name = "Система САПР"
        verbose_name_plural = "Системы САПР"
        ordering = ['category', 'name']
        unique_together = ['name', 'developer']

    def __str__(self):
        return f"{self.name} ({self.developer})"

    def get_price_display(self):
        if not self.price:
            return "Цена не указана"
        if self.license_type == 'subscription':
            return f"{self.price} ₽/год"
        elif self.license_type == 'free':
            return "Бесплатно"
        return f"{self.price} ₽"

    def get_platforms_list(self):
        return [p.strip() for p in self.platforms.split(',')] if self.platforms else []