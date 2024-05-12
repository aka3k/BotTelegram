#!/usr/bin/python

import telebot
import os
from pytube import YouTube

# Funzione per ottenere il token dal file token_bot.txt
def get_token():
    """
    Questa funzione legge il token del bot dal file token_bot.txt.
    """
    with open('token_bot.txt', 'r') as file:
        token = file.read().strip()
    return token

# Funzione per scaricare video da YouTube
def download_youtube_video(url, output_path):
    """
    Questa funzione scarica un video di YouTube all'indirizzo url nella cartella output_path.
    Restituisce il percorso completo del video scaricato.
    """
    yt = YouTube(url)
    # Scegli la migliore qualità disponibile
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    # Scarica il video
    filename = f"{video.title} ({video.resolution}).mp4"  # Aggiungi l'estensione del file
    video_path = os.path.join(output_path, filename)
    video.download(output_path, filename=filename)
    return video_path, video.resolution

# Ottieni il token
API_TOKEN = get_token()

# Ottieni il percorso della directory dello script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Crea la cartella di download se non esiste
download_dir = os.path.join(script_dir, "SucchiaVideoBot_download")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

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
            video_path, resolution = download_youtube_video(message.text, download_dir)
            # Invia il messaggio di conferma con la posizione del file e la risoluzione del video
            bot.reply_to(message, f"Video scaricato con successo!\nPosizione: {video_path}\nRisoluzione: {resolution}")
        except Exception as e:
            bot.reply_to(message, f"Si è verificato un errore durante il download del video: {str(e)}")
    else:
      bot.reply_to(message, """\
Ciao, sono Il SucchiaVideoBot.
Sono qui per aiutarti a scaricare video da YouTube.
Inviami il link del video di YouTube e io lo scaricherò per te!
""")
# Avvia il bot
bot.infinity_polling()
