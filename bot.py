
import os
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from db_manager import init_db 
from scheduler import start_scheduler

# Подтягивает токен из настроек Railway автоматически
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Используем твой домен на Railway для Mini App
    mini_app_url = "https://tgcall-production.up.railway.app/" 
    
    kb.add(
        types.KeyboardButton(
            text="📅 Open Calendar",
            web_app=types.WebAppInfo(url=mini_app_url)
        )
    )
    await message.answer(
        f"Привет! Нажми на кнопку, чтобы подключить календарь:", 
        reply_markup=kb
    )

if __name__ == "__main__":
    init_db() # Создаем базу данных для токенов
    start_scheduler() # Запускаем проверку календаря
    print("Бот запускается...")
    executor.start_polling(dp, skip_updates=True)
