import telebot
from pytube import YouTube
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

# Funzione per ottenere il token dal file token_bot.txt
def get_token():
    """
    Questa funzione legge il token del bot dal file token_bot.txt.
    """
    with open('token_bot.txt', 'r') as file:
        token = file.read().strip()
    return token

# Ottieni il token
API_TOKEN = get_token()

# Crea l'istanza del bot
bot = telebot.TeleBot(API_TOKEN)

# Messaggio iniziale del bot
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    """
    Questa funzione gestisce i comandi /start e /help.
    Il bot è progettato per aiutarti a scaricare video da YouTube.
    Invia il link del video di YouTube e il bot lo scaricherà per te.
    """
    bot.reply_to(message, """\
Ciao, sono Il SucchiaVideoBot.
Sono qui per aiutarti a scaricare video da YouTube.
Inviami il link del video di YouTube e io lo scaricherò per te!
""")

# Gestisci tutti gli altri messaggi di tipo 'text'
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    """
    Questa funzione gestisce tutti i messaggi di testo normali.
    """
    # Se il messaggio contiene un link di YouTube
    if 'youtube.com' in message.text:
        # Esegui il download del video
        try:
            # Scarica il video
            yt = YouTube(message.text)
            # Ottieni tutte le tracce video progressive
            video_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            
            # Crea la tastiera inline con i pulsanti per le varie risoluzioni
            keyboard = InlineKeyboardMarkup()
            for stream in video_streams:
                
                button_text = f"{stream.resolution} - {int(stream.filesize / (1024 * 1024))} MB"
                button_callback = f"download_{stream.resolution}_{message.text}"
                keyboard.add(InlineKeyboardButton(text=button_text, callback_data=button_callback))
            
            # Invia il messaggio con la tastiera inline
            bot.reply_to(message, "Scegli la risoluzione:", reply_markup=keyboard)
            
        except Exception as e:
            bot.reply_to(message, f"Si è verificato un errore durante il caricamento del video: {str(e)}")
    else:
        bot.reply_to(message, """\
Ciao, sono Il SucchiaVideoBot.
Sono qui per aiutarti a scaricare video da YouTube.
Inviami il link del video di YouTube e io lo scaricherò per te!
""")

# Gestisci i callback dai pulsanti inline
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """
    Questa funzione gestisce i callback dai pulsanti inline.
    """
    if call.data.startswith("download_"):
        resolution = call.data.split("_")[1]
        try:
            # Scarica il video con la risoluzione specificata
            yt = YouTube(call.data.split("_")[2])
            stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=resolution).first()
            video_data = requests.get(stream.url)
            if video_data.status_code == 200:
                bot.send_video(call.message.chat.id, video_data.content)
                bot.answer_callback_query(call.id, text=f"Video scaricato con successo in risoluzione {resolution}")
            else:
                bot.answer_callback_query(call.id, text="Impossibile scaricare il video al momento.")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Si è verificato un errore durante il download del video: {str(e)}")

# Avvia il bot
bot.infinity_polling()
