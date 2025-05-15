from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import CADSystem, Article, Category, FAQ, MigrationGuide
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CADSystemSerializer, FAQSerializer, MigrationGuideSerializer


# Веб-представления для шаблонов (оставлены без изменений)
class IndexView(TemplateView):
    template_name = 'myapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['popular_cads'] = CADSystem.objects.filter(is_featured=True)[:4]
        return context


class CADSystemListView(ListView):
    model = CADSystem
    template_name = 'myapp/cad_systems.html'
    context_object_name = 'cad_systems'

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category = self.request.GET.get('category')
        query = self.request.GET.get('q')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        developer = self.request.GET.get('developer')

        if category:
            queryset = queryset.filter(category__slug=category)
        if query:
            queryset = queryset.filter(name__icontains=query)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if developer:
            queryset = queryset.filter(developer__iexact=developer)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).values('slug', 'name')
        context['developers'] = CADSystem.objects.values('developer').distinct()
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


# API-представления для Telegram-бота
class CADSystemSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        cad_systems = CADSystem.objects.filter(
            Q(name__icontains=query) |
            Q(short_info__icontains=query) |
            Q(full_description__icontains=query) |
            Q(developer__icontains=query)
        ).filter(is_active=True)
        serializer = CADSystemSerializer(cad_systems, many=True)
        return Response(serializer.data)


class FAQSearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        faqs = FAQ.objects.filter(
            Q(question__icontains=query) |
            Q(keywords__icontains=query)
        )
        for faq in faqs:
            faq.usage_count += 1
            faq.save()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)


class MigrationGuideView(APIView):
    def get(self, request):
        query = request.GET.get('software', '')
        guides = MigrationGuide.objects.filter(
            foreign_software__icontains=query
        )
        serializer = MigrationGuideSerializer(guides, many=True)
        return Response(serializer.data)