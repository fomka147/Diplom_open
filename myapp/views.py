from django.views.generic import TemplateView, ListView, DetailView
from .models import CADSystem

class IndexView(TemplateView):
    template_name = 'myapp/index.html'

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