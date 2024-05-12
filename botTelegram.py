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

# Funzione per ottenere il percorso del desktop dell'utente
def get_user_desktop_dir():
  """
  Questa funzione restituisce il percorso della cartella desktop dell'utente.
  """
  if os.name == 'nt':  # Windows
    return os.path.join(os.path.expanduser('~'), 'Desktop')
  else:  # Linux o macOS
    return os.path.join(os.path.expanduser('~'), 'Desktop')

# Funzione per scaricare video da YouTube
def download_youtube_video(url, filename=None):
  """
  Questa funzione scarica un video di YouTube all'indirizzo url e lo salva nella cartella desktop dell'utente.
  Restituisce il percorso completo del video scaricato e la sua risoluzione.
  """
  yt = YouTube(url)
  # Scegli la migliore qualità disponibile
  video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
  # Scarica il video
  if not filename:
    filename = f"{video.title} ({video.resolution}).mp4"  # Aggiungi l'estensione del file
  user_desktop_dir = get_user_desktop_dir()
  if not os.path.exists(user_desktop_dir):
    os.makedirs(user_desktop_dir)
  video_path = os.path.join(user_desktop_dir, filename)
  video.download(video_path, filename=filename)
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
  Invia il link del video di YouTube e il bot lo scaricherà per te sulla tua scrivania!
  """
  bot.reply_to(message, """\
Ciao, sono Il SucchiaVideoBot.
Sono qui per aiutarti a scaricare video da YouTube.
Inviami il link del video di YouTube e io lo scaricherò per te sulla tua scrivania!
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
      video_path, resolution = download_youtube_video(message.text)
      # Invia il messaggio di conferma con la posizione del file e la risoluzione del video
      bot.reply_to(message, f"Video scaricato con successo sulla tua scrivania!\nPosizione: {video_path}\nRisoluzione: {resolution}")
    except Exception as e:
      bot.reply_to(message, f"Si è verificato un errore durante il download del video: {str(e)}")
  else:
    bot.reply_to(message, """\
Ciao, sono Il SucchiaVideoBot.
Sono qui per aiutarti a scaricare video da YouTube.
Inviami il link del video di YouTube e io lo scaricherò per te sulla tua scrivania!
""")

# Avvia il bot
bot.infinity_polling()

