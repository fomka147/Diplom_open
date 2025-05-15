import sys
import os
import logging
import django
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Проверяем текущий файл и его директорию
current_file = os.path.abspath(__file__)
logger.debug(f"Current file: {current_file}")

# Вычисляем корень проекта (D:\Diplom_open)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logger.debug(f"Calculated project root: {project_root}")

# Проверяем, существует ли папка myproject
myproject_path = os.path.join(project_root, 'myproject')
if not os.path.exists(myproject_path):
    logger.error(f"Папка myproject не найдена по пути: {myproject_path}")
    raise FileNotFoundError(f"Папка myproject не найдена: {myproject_path}")

# Проверяем наличие __init__.py в myproject
myproject_init = os.path.join(myproject_path, '__init__.py')
if not os.path.exists(myproject_init):
    logger.error(f"Файл __init__.py не найден в: {myproject_init}")
    raise FileNotFoundError(f"Файл __init__.py не найден в: {myproject_init}")

# Добавляем корень проекта в sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
logger.debug(f"sys.path after adding project root: {sys.path}")

# Настраиваем DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Проверяем доступность myproject
try:
    import myproject

    logger.info("Модуль myproject успешно импортирован")
except ImportError as e:
    logger.error(f"Не удалось импортировать myproject: {e}")
    raise

# Инициализируем Django
try:
    django.setup()
    logger.info("Django успешно инициализирован")
except Exception as e:
    logger.error(f"Ошибка инициализации Django: {e}")
    raise

from myapp.models import Subscription

# Локальный URL API
BASE_API_URL = 'http://127.0.0.1:8000/api/'

# Токен бота
BOT_TOKEN = '7730755045:AAE5vnf-YT3C_Vf4vcCpRarcAQIU6L2feXg'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Команда /start получена")
    await update.message.reply_text(
        "Привет! Я бот RusCAD. Используй команды:\n"
        "/find <название САПР> — поиск САПР\n"
        "/faq <вопрос> — ответы на вопросы\n"
        "/migrate <софт> — гид по миграции\n"
        "/subscribe <ключевое слово> — подписка на уведомления"
    )


async def find_sapr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    logger.info(f"Команда /find с запросом: {query}")
    if not query:
        await update.message.reply_text("Укажите название САПР, например: /find Компас-3D")
        return

    try:
        url = f'{BASE_API_URL}cad/search/?q={query}'
        logger.debug(f"Отправка запроса к API: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        cad_systems = response.json()
        logger.debug(f"Ответ API: {cad_systems}")

        if cad_systems:
            for cad in cad_systems:
                text = (
                    f"**{cad['name']}** ({cad['system_type']})\n"
                    f"Разработчик: {cad['developer']}\n"
                    f"{cad['short_info'] or cad['full_description'][:200]}\n"
                    f"Цена: {cad['price'] or 'Не указана'}\n"
                    f"Ссылка: {cad['official_url'] or 'Не указана'}\n"
                    f"Российская: {'Да' if cad['is_russian'] else 'Нет'}"
                )
                keyboard = [
                    [InlineKeyboardButton("Подписаться на обновления", callback_data=f"subscribe_{cad['name']}")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text("Ничего не найдено. Попробуйте другие ключевые слова.")
    except requests.RequestException as e:
        logger.error(f"Ошибка API: {e}")
        await update.message.reply_text(f"Ошибка при запросе к API: {e}")


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    logger.info(f"Команда /faq с запросом: {query}")
    if not query:
        await update.message.reply_text("Укажите вопрос, например: /faq машиностроение")
        return

    try:
        url = f'{BASE_API_URL}faq/search/?q={query}'
        logger.debug(f"Отправка запроса к API: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        faqs = response.json()
        logger.debug(f"Ответ API: {faqs}")

        if faqs:
            for faq in faqs:
                text = (
                    f"**{faq['question']}**\n"
                    f"{faq['answer']}\n"
                    f"Использовано: {faq['usage_count']} раз\n"
                    f"Источник: RusCAD (localhost)"
                )
                await update.message.reply_text(text, parse_mode='Markdown')
        else:
            await update.message.reply_text("Ответ не найден. Попробуйте переформулировать вопрос.")
    except requests.RequestException as e:
        logger.error(f"Ошибка API: {e}")
        await update.message.reply_text(f"Ошибка при запросе к API: {e}")


async def migrate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    software = ' '.join(context.args)
    logger.info(f"Команда /migrate с запросом: {software}")
    if not software:
        await update.message.reply_text("Укажите софт, например: /migrate AutoCAD")
        return

    try:
        url = f'{BASE_API_URL}migration/?software={software}'
        logger.debug(f"Отправка запроса к API: {url}")
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        guides = response.json()
        logger.debug(f"Ответ API: {guides}")

        if guides:
            for guide in guides:
                text = (
                    f"**Замена {guide['foreign_software']}**\n"
                    f"Аналоги: {guide['analogs']}\n"
                    f"Инструкция: {guide['instruction']}\n"
                    f"Подробности: localhost"
                )
                await update.message.reply_text(text, parse_mode='Markdown')
        else:
            await update.message.reply_text("Гид не найден. Попробуйте другой софт.")
    except requests.RequestException as e:
        logger.error(f"Ошибка API: {e}")
        await update.message.reply_text(f"Ошибка при запросе к API: {e}")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    logger.info(f"Команда /subscribe с запросом: {query}")
    if not query:
        await update.message.reply_text("Укажите ключевое слово, например: /subscribe AutoCAD")
        return

    telegram_id = str(update.message.from_user.id)
    Subscription.objects.create(telegram_id=telegram_id, keyword=query)
    await update.message.reply_text(f"Вы подписаны на уведомления по ключевому слову: {query}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    logger.info(f"Callback query: {data}")
    if data.startswith('subscribe_'):
        keyword = data.replace('subscribe_', '')
        telegram_id = str(query.from_user.id)
        Subscription.objects.create(telegram_id=telegram_id, keyword=keyword)
        await query.message.reply_text(f"Вы подписаны на уведомления по: {keyword}")
        await query.answer()


def main():
    logger.info("Запуск бота...")
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("find", find_sapr))
    application.add_handler(CommandHandler("faq", faq))
    application.add_handler(CommandHandler("migrate", migrate))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()