from django.views.generic import TemplateView, ListView, DetailView
from .models import CADSystem, Article

class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Выбираем 4 популярных САПР (например, по цене или категории)
        context['popular_cads'] = CADSystem.objects.all()[:4]
        return context

class CADSystemListView(ListView):
    model = CADSystem
    template_name = 'myapp/cad_systems.html'
    context_object_name = 'cad_systems'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [
            ('mechanical', 'Машиностроение'),
            ('architecture', 'Архитектура'),
            ('cnc', 'ЧПУ'),
            ('other', 'Другое'),
        ]
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

def get_queryset(self):
    queryset = super().get_queryset()
    category = self.request.GET.get('category')
    query = self.request.GET.get('q')
    if category:
        queryset = queryset.filter(category=category)
    if query:
        queryset = queryset.filter(name__icontains=query)
    return queryset