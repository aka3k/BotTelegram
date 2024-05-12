#!/usr/bin/python

import telebot
from pytube import YouTube
import requests
from io import BytesIO

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
            stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_url = stream.url
            # Carica il video direttamente su Telegram
            video_data = requests.get(video_url)
            if video_data.status_code == 200:
                bot.send_video(message.chat.id, video_data.content)
                # Invia il messaggio di conferma con la risoluzione del video
                bot.reply_to(message, f"Video inviato con successo!\nRisoluzione: {stream.resolution}")
            else:
                bot.reply_to(message, "Impossibile scaricare il video da YouTube al momento.")
        except Exception as e:
            bot.reply_to(message, f"Si è verificato un errore durante il caricamento del video: {str(e)}")
    else:
        bot.reply_to(message, """\
Ciao, sono Il SucchiaVideoBot.
Sono qui per aiutarti a scaricare video da YouTube.
Inviami il link del video di YouTube e io lo scaricherò per te!
""")

# Avvia il bot
bot.infinity_polling()
