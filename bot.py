import os
import telebot
from telebot import types
from dotenv import load_dotenv
from dto import Vacancy
from dto import Client
from services import ClientService
from messages import messages
from utils import is_string_an_url, normalize_url

load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))
clientService = ClientService()

def generate_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(messages.get('add_vacancy_button'))
    btn2 = types.KeyboardButton(messages.get('generate_report_button'))
    keyboard.add(btn1, btn2)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, messages.get('welcome_message'), reply_markup=generate_keyboard())

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    if is_string_an_url(normalize_url(message.text)):
        process_task_link(message)
        return
    if message.text == messages.get('add_vacancy_button'):
        reply = bot.send_message(message.chat.id, messages.get('send_link_message'))
        bot.register_next_step_handler(reply, process_task_link)
        return
    if message.text == messages.get('generate_report_button'):
        generate_report(message)
        return
    bot.send_message(message.chat.id, messages.get('select_action_message'), reply_markup=generate_keyboard())

def process_task_link(message):
    client = clientService.findByTelegramId(telegram_id=message.from_user.id)
    if not isinstance(client, Client):
        bot.send_message(message.chat.id, messages.get('you_not_our_client_message'))
        return
    try:
        link = normalize_url(message.text)
        if not is_string_an_url(link):
            bot.send_message(message.chat.id, messages.get('vacancy_link_is_not_valid_message'))
            return
        vacancy = Vacancy(link)
        clientService.createVacancyForClient(client=client, vacancy=vacancy)
        bot.send_message(message.chat.id, messages.get('vacancy_in_processing_message'))
    except RuntimeError as e:
        bot.send_message(message.chat.id, str(e))
    except Exception as e:
        bot.send_message(message.chat.id, messages.get('something_went_wrong_message'))

def generate_report(message):
    try:
        client = clientService.findByTelegramId(telegram_id=message.from_user.id)
        if not isinstance(client, Client):
            bot.send_message(message.chat.id, messages.get('you_not_our_client_message'))
            return
        if client.report_link != None and is_string_an_url(client.report_link):
            keyboard = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text=messages.get('report_link_button'), url=client.report_link)
            keyboard.add(btn1)
            bot.send_message(message.chat.id, messages.get('report_is_ready_message'), reply_markup=keyboard)
            return
        else:
            reply = bot.send_message(message.chat.id, messages.get('report_is_in_generating_message'))
            file = clientService.generateReportVacanciesForClient(client=client)
            bot.delete_message(message.chat.id, reply.id)
            bot.send_document(message.chat.id, document=file, caption=messages.get('report_is_ready_message'))
            return

            bot.send_message(message.chat.id, messages.get('report_is_not_ready_message'))
    except Exception as e:
        bot.send_message(message.chat.id, messages.get('something_went_wrong_message'))
        

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()