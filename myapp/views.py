from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import CADSystem

def index(request):
    return render(request, 'cad_sys/index.html')

class CADSystemListView(ListView):
    model = CADSystem
    template_name = 'cad_sys/cad_systems.html'
    context_object_name = 'page_obj'
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
    template_name = 'cad_sys/cad_detail.html'
    context_object_name = 'cad'

def contacts(request):
    return render(request, 'cad_sys/contacts.html')

def about(request):
    return render(request, 'cad_sys/about.html')