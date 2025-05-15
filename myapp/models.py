from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify as pytils_slugify


class Category(models.Model):
    name = models.CharField(max_length=100)  # Название категории САПР (например, "CAD для машиностроения")
    description = models.TextField(blank=True, null=True)  # Описание категории
    icon = models.CharField(max_length=50, blank=True, null=True)  # Иконка для категории
    color = models.CharField(max_length=20, blank=True, null=True)  # Цвет для категории
    slug = models.SlugField(max_length=100, unique=True)  # Уникальный slug для URL
    order = models.IntegerField(default=0)  # Порядок сортировки
    is_active = models.BooleanField(default=True)  # Активность категории

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']


class Feature(models.Model):
    name = models.CharField(max_length=100)  # Название функции САПР (например, "3D-моделирование")
    icon = models.CharField(max_length=50, blank=True, null=True)  # Иконка функции

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Feature"
        verbose_name_plural = "Features"
        ordering = ['name']


class CADSystem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cad_systems')  # Связь с категорией
    name = models.CharField(max_length=100)  # Название САПР (например, "Компас-3D")
    developer = models.CharField(max_length=100)  # Разработчик
    short_info = models.CharField(max_length=200, blank=True, null=True)  # Краткое описание
    full_description = models.TextField(blank=True, null=True)  # Полное описание
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Цена
    release_date = models.DateField(null=True, blank=True)  # Дата выпуска
    license_type = models.CharField(
        max_length=20,
        choices=[
            ('subscription', 'Подписка'),
            ('permanent', 'Постоянная'),
            ('free', 'Бесплатная'),
        ],
        default='subscription'
    )  # Тип лицензии
    is_russian = models.BooleanField(default=False)  # Российская ли САПР
    system_type = models.CharField(
        max_length=20,
        choices=[
            ('CAD', 'CAD'),
            ('CAE', 'CAE'),
            ('CAM', 'CAM'),
            ('PLM', 'PLM'),
        ],
        default='CAD'
    )  # Тип системы
    platforms = models.CharField(max_length=100, blank=True, null=True)  # Поддерживаемые платформы
    file_formats = models.CharField(max_length=100, blank=True, null=True)  # Поддерживаемые форматы файлов
    advantages = models.TextField(blank=True, null=True)  # Преимущества
    disadvantages = models.TextField(blank=True, null=True)  # Недостатки
    rating = models.FloatField(default=0.0)  # Рейтинг
    official_url = models.URLField(max_length=200, blank=True, null=True)  # Официальный сайт
    demo_url = models.URLField(max_length=200, blank=True, null=True)  # Ссылка на демо
    docs_url = models.URLField(max_length=200, blank=True, null=True)  # Ссылка на документацию
    is_active = models.BooleanField(default=True)  # Активность САПР
    is_featured = models.BooleanField(default=False)  # Рекомендуемая САПР
    slug = models.SlugField(max_length=100, unique=True, blank=True)  # Уникальный slug
    image = models.ImageField(upload_to='cad_images/', blank=True, null=True)  # Изображение
    features = models.ManyToManyField(Feature, blank=True)  # Связь с функциями
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания (для уведомлений)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = pytils_slugify(self.name) or slugify(self.name) or f"cad-{self.name.lower().replace(' ', '-')}"
            slug = base_slug
            counter = 1
            while CADSystem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "CAD System"
        verbose_name_plural = "CAD Systems"
        ordering = ['name']


class Article(models.Model):
    title = models.CharField(max_length=200)  # Заголовок статьи
    content = models.TextField()  # Содержание статьи
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Уникальный slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = pytils_slugify(self.title) or slugify(self.title) or f"article-{self.title.lower().replace(' ', '-')}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['-created_at']


class FAQ(models.Model):
    question = models.CharField(max_length=200)  # Вопрос (например, "Какой софт для машиностроения?")
    answer = models.TextField()  # Ответ
    keywords = models.CharField(max_length=200, blank=True)  # Ключевые слова для поиска
    usage_count = models.PositiveIntegerField(default=0)  # Счетчик использования
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']


class Subscription(models.Model):
    telegram_id = models.CharField(max_length=50)  # Telegram ID пользователя
    keyword = models.CharField(max_length=100)  # Ключевое слово для подписки
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания подписки

    def __str__(self):
        return f"{self.telegram_id}: {self.keyword}"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ['-created_at']


class MigrationGuide(models.Model):
    foreign_software = models.CharField(max_length=100)  # Зарубежный софт (например, "AutoCAD")
    analogs = models.CharField(max_length=200)  # Российские аналоги (например, "Компас-3D, NanoCAD")
    instruction = models.TextField()  # Инструкция по миграции (Markdown)
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return self.foreign_software

    class Meta:
        verbose_name = "Migration Guide"
        verbose_name_plural = "Migration Guides"
        ordering = ['-created_at']