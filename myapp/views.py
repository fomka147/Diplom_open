from django.views.generic import TemplateView, ListView, DetailView
from .models import CADSystem, Article
from django.db.models import Q

class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_cads'] = CADSystem.objects.all()[:4]
        return context

class CADSystemListView(ListView):
    model = CADSystem
    template_name = 'myapp/cad_systems.html'
    context_object_name = 'cad_systems'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        query = self.request.GET.get('q')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        manufacturer = self.request.GET.get('manufacturer')

        if category:
            queryset = queryset.filter(category=category)
        if query:
            queryset = queryset.filter(name__icontains=query)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if manufacturer:
            queryset = queryset.filter(manufacturer__iexact=manufacturer)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [
            ('mechanical', 'Машиностроение'),
            ('architecture', 'Архитектура'),
            ('cnc', 'ЧПУ'),
            ('other', 'Другое'),
        ]
        context['manufacturers'] = CADSystem.objects.values('manufacturer').distinct()
        return context

class CADSystemDetailView(DetailView):
    model = CADSystem
    template_name = 'myapp/cad_detail.html'
    context_object_name = 'cad'

class ContactsView(TemplateView):
    template_name = 'myapp/contacts.html'

class AboutView(TemplateView):
    template_name = 'myapp/about.html'

class ArticleListView(ListView):
    model = Article
    template_name = 'myapp/articles.html'
    context_object_name = 'articles'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'myapp/article_detail.html'
    context_object_name = 'article'