from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from telegram.ext.updater import Updater
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from translate import Translator
from deep_translator import GoogleTranslator
def start_s(update: Update , context: CallbackContext) -> None:
    # keyboard = [
    #     ["/select_lang"]
    # ]
    # reply_markup1 = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    keyboard = [
        [
            InlineKeyboardButton("German", callback_data="German"),
            InlineKeyboardButton("English", callback_data="English"),
            InlineKeyboardButton("Persian", callback_data="Persian")
        ]
    ]
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    reply_markup = InlineKeyboardMarkup(keyboard)
    s1 = "سلام. خوش آمدید" 
    s2= "این ربات از گوگل ترنسلیت جهت ترجمه متون استفاده میکند."
    s3 = "لطفا زبانی که به آن میخواهید ترجمه کنید را انخاب کرده و سپس کلمه یا متن مورد نظر خود را تایپ کنید."
    update.message.reply_text(f"{s1}\n{s2}\n{s3}",reply_markup = reply_markup)

def select_lang(update: Update , context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("German", callback_data="German"),
            InlineKeyboardButton("English", callback_data="English"),
            InlineKeyboardButton("Persian", callback_data="Persian")
        ]
    ]
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    reply_markup = InlineKeyboardMarkup(keyboard)
    s1 = "زبانی که به میخواهید ترجمه کنید را انتخاب کنید." 
    update.message.reply_text(f"{s1}",reply_markup = reply_markup)


proxies_example = {
    "https": "34.195.196.27:8080",
    "http": "34.195.196.27:8080"
}
lang =""
def button(update:Update, context: CallbackContext)-> None:
    global lang
    user_id = update.effective_user.id
    lang = update.callback_query.data.lower()
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    context.user_data["lang"][user_id] = lang
    query = update.callback_query
    query.answer()
    if lang == "german": query.edit_message_text("ترجمه از هر زبانی به زبان آلمانی انتخاب شد.")
    elif lang =="english": query.edit_message_text("ترجمه از هر زبانی به زبان انگلیسی انتخاب شد.")
    elif lang =="persian": query.edit_message_text("ترجمه از هر زبانی به زبان فارسی انتخاب شد.")
    # query.edit_message_text(text= f"{query.data} has been selected")

def lang_translator(user_input):
    global lang
    translate_to = ""
    if lang == "german": translate_to = "de"
    elif lang =="english": translate_to = "en"
    elif lang =="persian": translate_to = "fa"
    translated = GoogleTranslator(source='auto', target=translate_to).translate(user_input)
    #translator = Translator(from_lang = "english" , to_lang= lang)
    #translation = translator.translate(user_input)
    return translated


def reply(update, context):
    global lang
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    user_id = update.effective_user.id
    lang = context.user_data["lang"].get(user_id)
    if not lang:
        select_lang(update, context)
    else:
        user_input = update.message.text
        update.message.reply_text(lang_translator(user_input=user_input))


def main():
    api = open("api.txt", "r")
    updater = Updater(api.read(), use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(('start'),start_s))
    dp.add_handler(CommandHandler('selectlanguage',select_lang))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text, reply))
    updater.start_polling()
    updater.idle()

main()