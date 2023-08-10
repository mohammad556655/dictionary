from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, Bot
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext.updater import Updater
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from translate import Translator
from deep_translator import GoogleTranslator
import speech_recognition as sr
import whisper
from gtts import gTTS
from gtts import lang as gttslang
import io
from langdetect import detect
import os
import threading
from textblob import TextBlob

lock = threading.Lock()
model = whisper.load_model('base')
# from langdetect import detect
REPLIED_LANG, MY_LANG = range(2)
ASK_TO_CHANGE_MODE = range(1)
def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    speech_stream = io.BytesIO()
    tts.write_to_fp(speech_stream)
    return speech_stream.getvalue()
def start_s(update: Update , context: CallbackContext) -> None:
    # keyboard = [
    #     ["/select_lang"]
    # ]
    # reply_markup1 = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    keyboard1 = [
        [
            InlineKeyboardButton("German", callback_data="German"),
            InlineKeyboardButton("English", callback_data="English"),
            InlineKeyboardButton("Persian", callback_data="Persian"),
            InlineKeyboardButton("Russian", callback_data="Russian"),
            InlineKeyboardButton("Spanish", callback_data="Spanish")
        ]
    ]
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    if "mylang" not in context.user_data:
        context.user_data["mylang"] = {}
        context.user_data["mylang"][user_id] = "fa"
    if "mode" not in context.user_data:
        context.user_data["mode"] = {}
        context.user_data["mode"][user_id] = "translate"
    reply_markup1 = InlineKeyboardMarkup(keyboard1)
    s1 = "سلام. خوش آمدید" 
    s2= "این ربات از گوگل ترنسلیت جهت ترجمه متون استفاده میکند."
    s3 = "لطفا زبانی که به آن میخواهید ترجمه کنید را انخاب کرده و سپس کلمه یا متن مورد نظر خود را تایپ کنید."
    update.message.reply_text(f"{s1}\n{s2}\n{s3}",reply_markup = reply_markup1)

def select_lang(update: Update , context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("German", callback_data="German"),
            InlineKeyboardButton("English", callback_data="English"),
            InlineKeyboardButton("Persian", callback_data="Persian"),
            InlineKeyboardButton("Russian", callback_data="Russian"),
            InlineKeyboardButton("Spanish", callback_data="Spanish")
        ]
    ]
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    if "mylang" not in context.user_data:
        context.user_data["mylang"] = {}
        context.user_data["mylang"][user_id] = "fa"
    if "mode" not in context.user_data:
        context.user_data["mode"] = {}
        context.user_data["mode"][user_id] = "translate"
    reply_markup = InlineKeyboardMarkup(keyboard)
    s1 = "زبانی که به میخواهید ترجمه کنید را انتخاب کنید." 
    update.message.reply_text(f"{s1}",reply_markup = reply_markup)
def ask_my_language(update: Update , context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    if "mylang" not in context.user_data:
        context.user_data["mylang"] = {}
        context.user_data["mylang"][user_id] = "fa"
    if "mode" not in context.user_data:
        context.user_data["mode"] = {}
        context.user_data["mode"][user_id] = "translate"
    update.message.reply_text(f'زبان پیشفرض شما {context.user_data["mylang"][user_id]} میباشد')
    update.message.reply_text("برای تغییر زبان پیشفرض /change را کلیک کنید ")
    return REPLIED_LANG

def my_language(update: Update , context: CallbackContext) -> None:
    update.message.reply_text('زبان پیشفرض جدید را وارد کنید')
    

    return MY_LANG
    # if  == "farsi" or update.message.reply_to_message.text == "فارسی" or update.message.reply_to_message.text == "persian":
    #     context.user_data["mylang"][user_id] = "fa"
    # update.message.reply_text("زبان پیشفرض خود را وارد کنید.")
def save_my_language(update: Update , context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    if "mylang" not in context.user_data:
        context.user_data["mylang"] = {}
        context.user_data["mylang"][user_id] = "fa"
    if "mode" not in context.user_data:
        context.user_data["mode"] = {}
        context.user_data["mode"][user_id] = "translate"
    langu = update.message.text

    if langu == "farsi" or langu == "فارسی" or langu == "persian":
        context.user_data["mylang"][user_id] = "fa"
        update.message.reply_text(f'زبان پیشفرض به {context.user_data["mylang"][user_id]} تغییر یافت')
    elif langu == "انگلیسی" or langu.lower() == "english":
        context.user_data["mylang"][user_id] = "en"
        update.message.reply_text(f'زبان پیشفرض به {context.user_data["mylang"][user_id]} تغییر یافت')
    elif langu == "آلمانی" or langu.lower() == "german":
        context.user_data["mylang"][user_id] = "de"
        update.message.reply_text(f'زبان پیشفرض به {context.user_data["mylang"][user_id]} تغییر یافت')
    else:
        update.message.reply_text("مقدار وارد شده اشتباه است. لطفا دوباره زبان پیشفرض جدید را وارد کنید")
        return MY_LANG
    return ConversationHandler.END

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
    if "mylang" not in context.user_data:
        context.user_data["mylang"] = {}
        context.user_data["mylang"][user_id] = "fa"
    if "mode" not in context.user_data:
        context.user_data["mode"] = {}
        context.user_data["mode"][user_id] = "translate"
    context.user_data["lang"][user_id] = lang
    query = update.callback_query
    query.answer()
    if lang == "german": query.edit_message_text("ترجمه از هر زبانی به زبان آلمانی انتخاب شد.")
    elif lang =="english": query.edit_message_text("ترجمه از هر زبانی به زبان انگلیسی انتخاب شد.")
    elif lang =="persian": query.edit_message_text("ترجمه از هر زبانی به زبان فارسی انتخاب شد.")
    elif lang =="russian": query.edit_message_text("ترجمه از هر زبانی به زبان روسی انتخاب شد.")
    elif lang =="spanish": query.edit_message_text("ترجمه از هر زبانی به زبان اسپانیایی انتخاب شد.")
    
    # query.edit_message_text(text= f"{query.data} has been selected")

def lang_translator(user_input):
    global lang
    translate_to = ""
    if lang == "german": translate_to = "de"
    elif lang =="english": translate_to = "en"
    elif lang =="persian": translate_to = "fa"
    elif lang =="spanish": translate_to = "es"
    elif lang =="russian": translate_to = "ru"
    translated = GoogleTranslator(source='auto', target=translate_to).translate(user_input)

    #translator = Translator(from_lang = "english" , to_lang= lang)
    #translation = translator.translate(user_input)
    return translated


def reply(update, context):
    with lock:
        global lang
        global model
        user_id = update.effective_user.id
        if "lang" not in context.user_data:
            context.user_data["lang"] = {}
        if "mylang" not in context.user_data:
            context.user_data["mylang"] = {}
            context.user_data["mylang"][user_id] = "fa"
        if "mode" not in context.user_data:
            context.user_data["mode"] = {}
            context.user_data["mode"][user_id] = "translate"
        
        lang = context.user_data["lang"].get(user_id)
        if not lang:
            select_lang(update, context)
        else:
            if context.user_data["mode"].get(user_id) == "translate":
                if update.message.text:
                    translate_to =""
                    if lang == "german": translate_to = "de"
                    elif lang =="english": translate_to = "en"
                    elif lang =="persian": translate_to = "fa"
                    elif lang =="russian": translate_to = "ru"
                    elif lang =="spanish": translate_to = "es"
                    user_input = update.message.text
                    translated = lang_translator(user_input=user_input)
                    update.message.reply_text(translated)
                    if translate_to!="fa" and translate_to!="es":
                        speech_data = text_to_speech(translated, lang=translate_to)
                        update.message.reply_voice(voice=speech_data)
                
                
                
                elif update.message.audio:
                    audio = update.message.audio.get_file()
                    file_extension = audio.file_path.split(".")[-1]  # Get the file extension from the file_path
                    audio.download(str(user_id) + "." + file_extension)  # Save with the correct file extension
                    main_path =str(user_id) + "." + file_extension
                    
                    
                    audios = whisper.load_audio(main_path)
                    audios = whisper.pad_or_trim(audios)
                    mel = whisper.log_mel_spectrogram(audios).to(model.device)
                    _, probs = model.detect_language(mel)
                    audio_laguages= {max(probs, key=probs.get)}


                    # decode the audio
                    options = whisper.DecodingOptions(fp16 = False)
                    result = whisper.decode(model, mel, options)

                    # print the recognized text
                    update.message.reply_text(f'زبان فایل: \n {str(next(iter(audio_laguages)))}')
                    update.message.reply_text(f'متن اصلی فایل: \n {result.text}')
                    update.message.reply_text(f'ترجمه متن فایل: \n {lang_translator(result.text)}')
                    os.remove(main_path)

                    # Handling voice messages
                    # Handling voice messages

                    # audio_wav = AudioSegment.from_file(str(user_id) + "." + file_extension, format=file_extension)
                    # wav_file_path = str(user_id) + ".wav"
                    # audio_wav.export(wav_file_path, format="wav")
                    # # Perform speech-to-text on the audio and translate the text
                    # recognizer = sr.Recognizer()
                    # with sr.AudioFile(wav_file_path) as source:  # Use the correct file extension
                    #     audio_data = recognizer.record(source)
                    #     audio_text = recognizer.recognize_google(audio_data)
                    #     print(audio_text)
                    #     update.message.reply_text(lang_translator(user_input=audio_text, lang=lang))
                elif update.message.voice:
                    audio = update.message.voice.get_file()
                    file_extension = audio.file_path.split(".")[-1]  # Get the file extension from the file_path
                    audio.download(str(user_id) + "." + file_extension)  # Save with the correct file extension
                    main_path =str(user_id) + "." + file_extension
                    
                    
                    
                    
                    audios = whisper.load_audio(main_path)
                    audios = whisper.pad_or_trim(audios)
                    mel = whisper.log_mel_spectrogram(audios).to(model.device)
                    _, probs = model.detect_language(mel)
                    voice_laguages= {max(probs, key=probs.get)}
                    

                    # decode the audio
                    options = whisper.DecodingOptions(fp16 = False)
                    result = whisper.decode(model, mel, options)

                    # print the recognized text
                    update.message.reply_text(f'زبان فایل: \n {str(next(iter(voice_laguages)))}')
                    update.message.reply_text(f'متن اصلی فایل: \n {result.text}')
                    update.message.reply_text(f'ترجمه متن فایل: \n {lang_translator(result.text)}')
                    os.remove(main_path)

                    # Handling voice messages
                    # Handling voice messages
                    # audio = update.message.voice.get_file()
                    # file_extension = audio.file_path.split(".")[-1]  # Get the file extension from the file_path
                    # audio.download(str(user_id) + "." + file_extension)  # Save with the correct file extension
                    # # audio_wav = AudioSegment.from_file(str(user_id) + "." + file_extension, format=file_extension)
                    # wav_file_path = str(user_id) + ".wav"
                    # main_path =str(user_id) + "." + file_extension
                    # # audio_wav.export(wav_file_path, format="wav")
                    # # Perform speech-to-text on the audio and translate the text
                    # recognizer = sr.Recognizer()
                    # with sr.AudioFile(main_path) as source:  # Use the correct file extension
                    #     audio_data = recognizer.record(source)
                    #     audio_text = recognizer.recognize_google(audio_data)
                    #     print(audio_text)
                    #     update.message.reply_text(lang_translator(user_input=audio_text, lang=lang))
                elif update.message.document:
                    # Handling video messages
                    # Extract text from video if necessary
                    update.message.reply_text("Video received. Text extraction is not implemented yet")
                elif update.message.video:
                    # Handling video messages
                    # Extract text from video if necessary
                    update.message.reply_text("Video received. Text extraction is not implemented yet")
            elif context.user_data["mode"].get(user_id) == "pronounciation":
                if update.message.text:
                    # translate_to =""
                    if lang == "german": translate_to = "de"
                    elif lang =="english": translate_to = "en"
                    elif lang =="persian": translate_to = "fa"
                    elif lang =="russian": translate_to = "ru"
                    elif lang =="spanish": translate_to = "es"
                    user_input = update.message.text
                    # translated = lang_translator(user_input=user_input)
                    # update.message.reply_text(translated)
                    # if translate_to!="fa" and translate_to!="es":
                    # b = TextBlob(user_input)
                    gtts_langs = gttslang.tts_langs()
                    # language_given = b.detect_language()
                    language_given = detect(user_input)
                    
                    if language_given in gtts_langs:
                    
                        
                        speech_data = text_to_speech(user_input, lang=language_given)
                        update.message.reply_voice(voice=speech_data)
                    else:
                        update.message.reply_text("زبان متن وارد شده پشتیبانی نمیشود")
                

def ask_change_mode(update: Update , context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if "lang" not in context.user_data:
        context.user_data["lang"] = {}
    if "mylang" not in context.user_data:
        context.user_data["mylang"] = {}
        context.user_data["mylang"][user_id] = "fa"
    if "mode" not in context.user_data:
        context.user_data["mode"] = {}
        context.user_data["mode"][user_id] = "translate"

    if context.user_data["mode"][user_id] == "translate":
    
        update.message.reply_text(f'حالت پیشفرض شما ترجمه میباشد')
        update.message.reply_text("برای تغییر حالت پیشفرض /yes را کلیک کنید ")
    elif context.user_data["mode"][user_id] == "pronounciation" :
        update.message.reply_text(f'حالت پیشفرض شما تلفظ میباشد')
        update.message.reply_text("برای تغییر حالت پیشفرض /yes را کلیک کنید ")

    return ASK_TO_CHANGE_MODE

def change_mode(update: Update , context: CallbackContext) -> None:
    user_id = update.effective_user.id
    mode = context.user_data["mode"][user_id]

    if mode == "translate":
        context.user_data["mode"][user_id] = "pronounciation"

    elif mode == "pronounciation":
        context.user_data["mode"][user_id] = "translate"


    if context.user_data["mode"][user_id] == "translate":
        update.message.reply_text(f'حالت پیشفرض شما به ترجمه تغییر یافت')
    elif context.user_data["mode"][user_id] == "pronounciation" :
        update.message.reply_text(f'حالت پیشفرض شما به تلفظ تغییر یافت')
    return ConversationHandler.END

def main():
    api = open("api.txt", "r")
    updater = Updater(api.read(), use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(('start'),start_s,run_async=True))
    dp.add_handler(CommandHandler('selectlanguage',select_lang,run_async=True))
    dp.add_handler(CallbackQueryHandler(button))
    change_default_lang_conv = ConversationHandler(
        entry_points = [CommandHandler('mylanguage', ask_my_language,run_async=True)],
        fallbacks=[],

        states={
            REPLIED_LANG: [CommandHandler('change', my_language,run_async=True)],
            MY_LANG: [MessageHandler(Filters.text, save_my_language,run_async=True)],
        },
    )
    dp.add_handler(change_default_lang_conv)


    change_mode_conv = ConversationHandler(
        entry_points = [CommandHandler('changemode', ask_change_mode,run_async=True)],
        fallbacks=[],

        states={
            ASK_TO_CHANGE_MODE: [CommandHandler('yes', change_mode,run_async=True)],
        },
    )
    dp.add_handler(change_mode_conv)
    dp.add_handler(MessageHandler(Filters.audio | Filters.voice | Filters.text | Filters.document, reply,run_async=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
