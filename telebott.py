import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from openai import OpenAI

# Store previous response
class Reference:
    def __init__(self):
        self.response = ""

reference = Reference()

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("Telegram BOT Token not found in .env file!")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in .env file!")

# Initialize bot, dispatcher, and OpenAI client
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = "gpt-3.5-turbo"

def clear_past():
    reference.response = ""

# --- Handlers ---
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Hi! I am Tele Bot. How can I help you?")

@dp.message(Command("clear"))
async def clear(message: types.Message):
    clear_past()
    await message.answer("✅ Conversation history cleared!")

@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("""
Available commands:
/start - Start the bot
/clear - Clear chat history
/help - Show this help
""")

@dp.message(F.text)
async def chatgpt(message: types.Message):
    print(f"User: {message.text}")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": message.text}
        ]
    )

    reply = response.choices[0].message.content
    reference.response = reply
    print(f"ChatGPT: {reply}")

    await message.answer(reply)

# --- Run Bot ---
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
