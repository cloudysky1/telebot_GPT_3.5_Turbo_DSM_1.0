import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Check token
if API_TOKEN is None:
    raise ValueError("BOT_TOKEN not found in .env. Check your .env file!")

print("Loaded BOT_TOKEN:", API_TOKEN)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Create Bot, Dispatcher, and Router
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Start command handler
@router.message(Command(commands=["start", "help"]))
async def command_start_handler(message: types.Message):
    await message.answer("Hi 👋\nI am Echo Bot!\nPowered by aiogram v3.")

# Echo any message
@router.message()
async def echo_handler(message: types.Message):
    await message.answer(message.text)

# Run the bot
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
