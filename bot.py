import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from db_manager import init_db
from scheduler import start_scheduler

# Настройка логов (будут видны в Railway Logs)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    logger.error("ОШИБКА: BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    # Railway домен, где крутится наш index.html
    mini_app_url = "https://tgcall-production.up.railway.app/"
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        types.KeyboardButton(
            text="📅 Открыть календарь",
            web_app=types.WebAppInfo(url=mini_app_url)
        )
    )
    
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Нажми кнопку ниже, чтобы авторизовать Google Календарь.",
        reply_markup=kb
    )

def on_startup(_):
    init_db()          # Инициализируем БД
    start_scheduler()  # Запускаем планировщик
    logger.info("Бот успешно запущен и готов к работе!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
