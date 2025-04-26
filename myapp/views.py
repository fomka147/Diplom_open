from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, CADSystem


def index(request):
    """Главная страница со всеми категориями и системами"""
    categories = Category.objects.filter(is_active=True).order_by('order')
    featured_systems = CADSystem.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category')[:6]

    # Получаем системы для каждой категории (по 3 на категорию)
    categorized_systems = {}
    for category in categories:
        systems = category.systems.filter(is_active=True)[:3]
        if systems:
            categorized_systems[category] = systems

    context = {
        'categories': categories,
        'featured_systems': featured_systems,
        'categorized_systems': categorized_systems,
        'all_systems_count': CADSystem.objects.filter(is_active=True).count(),
    }
    return render(request, 'myapp/index.html', context)


def category_detail(request, slug):
    """Детальная страница категории со всеми системами"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    systems = category.systems.filter(is_active=True).select_related('category')

    # Фильтрация по параметрам
    system_type = request.GET.get('type')
    license_type = request.GET.get('license')
    is_russian = request.GET.get('russian')

    if system_type:
        systems = systems.filter(system_type=system_type)
    if license_type:
        systems = systems.filter(license_type=license_type)
    if is_russian:
        systems = systems.filter(is_russian=(is_russian == 'true'))

    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_asc':
        systems = systems.order_by('price')
    elif sort_by == 'price_desc':
        systems = systems.order_by('-price')
    elif sort_by == 'rating':
        systems = systems.order_by('-rating')
    else:
        systems = systems.order_by('name')

    context = {
        'category': category,
        'systems': systems,
        'system_types': CADSystem.TYPE_CHOICES,
        'license_types': CADSystem.LICENSE_CHOICES,
        'current_filters': {
            'system_type': system_type,
            'license_type': license_type,
            'is_russian': is_russian,
            'sort_by': sort_by,
        }
    }
    return render(request, 'myapp/category_detail.html', context)


def system_detail(request, slug):
    """Детальная страница конкретной системы"""
    system = get_object_or_404(CADSystem, slug=slug, is_active=True)
    context = {
        'system': system
    }
    return render(request, 'myapp/system_detail.html', context)


def search(request):
    """Поиск систем по названию"""
    query = request.GET.get('q')
    systems = []
    if query:
        systems = CADSystem.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        ).filter(is_active=True)
    context = {
        'systems': systems,
        'query': query,
    }
    return render(request, 'myapp/search_results.html', context)
