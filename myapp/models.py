from django.db import models
from django.utils.text import slugify

class CADSystem(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('mechanical', 'Машиностроение'),
        ('architecture', 'Архитектура'),
        ('cnc', 'ЧПУ'),
        ('other', 'Другое'),
    ])
    description = models.TextField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cad_images/', blank=True, null=True)
    release_date = models.DateField()
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=['name', 'category'])]