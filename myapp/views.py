from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import CADSystem

def index(request):
    return render(request, 'myapp/index.html')

class CADSystemListView(ListView):
    model = CADSystem
    template_name = 'myapp/cad_systems.html'
    context_object_name = 'cad_systems'
    paginate_by = 10

    def get_queryset(self):
        queryset = CADSystem.objects.all()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        if query:
            queryset = queryset.filter(name__icontains=query)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['category'] = self.request.GET.get('category', '')
        context['categories'] = CADSystem._meta.get_field('category').choices
        return context

class CADSystemDetailView(DetailView):
    model = CADSystem
    template_name = 'myapp/cad_detail.html'
    context_object_name = 'cad'

def contacts(request):
    return render(request, 'myapp/contacts.html')

def about(request):
    return render(request, 'myapp/about.html')