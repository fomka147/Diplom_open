from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import CADSystemSearchView, FAQSearchView, MigrationGuideView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls', namespace='myapp')),
    # API-маршруты для Telegram-бота
    path('api/cad/search/', CADSystemSearchView.as_view(), name='cad-search'),
    path('api/faq/search/', FAQSearchView.as_view(), name='faq-search'),
    path('api/migration/', MigrationGuideView.as_view(), name='migration-guide'),
]

# Обслуживание медиа-файлов (для изображений CADSystem)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обслуживание статических файлов только в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)