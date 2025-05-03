from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify as pytils_slugify
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Feature(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

class CADSystem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    short_info = models.CharField(max_length=200, blank=True, null=True)
    full_description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    license_type = models.CharField(max_length=20, choices=[
        ('subscription', 'Подписка'),
        ('permanent', 'Постоянная'),
        ('free', 'Бесплатная'),
    ], default='subscription')
    is_russian = models.BooleanField(default=False)
    system_type = models.CharField(max_length=20, choices=[
        ('CAD', 'CAD'),
        ('CAE', 'CAE'),
        ('CAM', 'CAM'),
        ('PLM', 'PLM'),
    ], default='CAD')
    platforms = models.CharField(max_length=100, blank=True, null=True)
    file_formats = models.CharField(max_length=100, blank=True, null=True)
    advantages = models.TextField(blank=True, null=True)
    disadvantages = models.TextField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    official_url = models.URLField(max_length=200, blank=True, null=True)
    demo_url = models.URLField(max_length=200, blank=True, null=True)
    docs_url = models.URLField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='cad_images/', blank=True, null=True)
    features = models.ManyToManyField(Feature, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = pytils_slugify(self.name)
            if not base_slug:
                base_slug = f"cad-{self.name.lower().replace(' ', '-')}"
            slug = base_slug
            counter = 1
            while CADSystem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = pytils_slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title