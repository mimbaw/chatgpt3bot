from threading import Thread

from telebot.async_telebot import AsyncTeleBot
from telebot import TeleBot
from telebot.types import Message

from backend.main import MessageHandler, clear_dialog
from config import BOT_TOKEN



bot = AsyncTeleBot(BOT_TOKEN)
sync_bot = TeleBot(BOT_TOKEN)

users_state_dict = dict()



@bot.message_handler(commands=['clear_dialog']) 
async def handler(message: Message):
    clear_dialog(str(message.from_user.id))
    await bot.send_message(message.from_user.id, "Диалог успешно сброшен")


@bot.message_handler(commands=['start'])
async def handler(message: Message):
    await bot.send_message(message.chat.id, 'Страртовал')


@bot.message_handler(content_types='text')
async def handler(message: Message):
    if message.chat.id in users_state_dict:
        if users_state_dict[message.chat.id]:
            await bot.delete_message(message.chat.id, message.message_id)
            await bot.send_message(message.chat.id, 'Если нейросеть молчит, не перебивай её')
            return
    await bot.send_message(message.chat.id, 'Думаю...')
    users_state_dict[message.chat.id] = True
    Thread(target=process_answer, args=(message, )).start()


def process_answer(message: Message) -> None:
    """
    Отдельная функция, задающая вопрос ChatGPT.
    Запускается отдельным потоком для лучшей оптимизации
    """
    string = MessageHandler(str(message.from_user.id)).question(message.text)
    sync_bot.send_message(message.chat.id, string, reply_to_message_id=message.message_id)
    users_state_dict[message.chat.id] = False



async def start_bot() -> None:
    """
    Запускает бота
    """
    await bot.infinity_polling()