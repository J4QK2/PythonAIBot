from aiogram import Bot, Dispatcher
from aiogram.types import Message
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# загружает переменные из окружения
load_dotenv()

# создаем объект бота, и создаем диспетчера для обработки сообщения от пользователя
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# читаем промпт
with open("prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# анализируем сообщение с помощью GPT-5 mini, как входные данные загружаем SYSTEM_PROMPT
@dp.message()
async def cmd_ai(message: Message):
    response = await client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message.text
            }
        ]
    )

    await message.answer(response.output_text)




async def main():
    await dp.start_polling(bot)

# запуск бота
if __name__ == '__main__':
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt():
        pass