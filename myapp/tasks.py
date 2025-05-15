from celery import shared_task
from django.utils import timezone
from .models import Subscription, CADSystem
from telegram import Bot


@shared_task
def check_new_saprs():
    bot = Bot(token='7730755045:AAE5vnf-YT3C_Vf4vcCpRarcAQIU6L2feXg')
    new_saprs = CADSystem.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=1))

    for sapr in new_saprs:
        subscriptions = Subscription.objects.filter(keyword__icontains=sapr.name)
        for sub in subscriptions:
            text = (
                f"Новое САПР: {sapr.name} ({sapr.system_type})\n"
                f"Разработчик: {sapr.developer}\n"
                f"{sapr.short_info or sapr.full_description[:200]}\n"
                f"Цена: {sapr.price or 'Не указана'}\n"
                f"Ссылка: {sapr.official_url or 'Не указана'}\n"
                f"Российская: {'Да' if sapr.is_russian else 'Нет'}"
            )
            bot.send_message(chat_id=sub.telegram_id, text=text, parse_mode='Markdown')