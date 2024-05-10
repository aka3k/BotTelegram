import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube

def start(update, context):
  """
  Funzione per il comando /start.
  - Presenta il bot e le sue funzionalità.
  - Include un avviso sul copyright.
  - Spiega come caricare il token da un file separato.
  """
  update.message.reply_text(
      """
      Benvenuto nel Bot di Download Video di YouTube!

      Inviami il link di un video di YouTube e lo scaricherò per te in alta risoluzione.

      **ATTENZIONE:**

      * Scaricare contenuti protetti da copyright senza permesso è illegale. Usa questo bot solo per scopi didattici e assicurati di rispettare le normative sul copyright.
      * Per utilizzare questo bot, devi creare un file chiamato "token_bot" nella stessa cartella del programma e inserire al suo interno il tuo token Telegram.

      Per iniziare, invia il link di un video YouTube.
      """,
      parse_mode=telegram.ParseMode.HTML
  )

def download_video(update, context):
  """
  Funzione per il download di video.
  - Scarica il video con la migliore risoluzione disponibile (progressiva).
  - Gestisce gli errori e fornisce feedback all'utente.
  - Salva il video nella cartella "downloads".
  """
  try:
    # Recupera il link del video dal messaggio
    url = update.message.text

    # Crea la cartella "downloads" se non esiste
    if not os.path.exists("downloads"):
      os.makedirs("downloads")

    # Ottieni il video da YouTube
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    # Controlla se il video è disponibile
    if video is None:
      update.message.reply_text("Nessun video disponibile per il download.")
      return

    # Recupera il nome del file e la sua estensione
    filename = video.title + "." + video.extension

    # Salva il video nella cartella "downloads"
    video.download(filename="downloads/" + filename)

    # Informa l'utente del download completato
    update.message.reply_text(f"Video scaricato con successo! Salvato in 'downloads/{filename}'.")

  except Exception as e:
    # Gestisce gli errori e fornisce feedback all'utente
    error_message = f"Si è verificato un errore durante il download del video: {e}"
    update.message.reply_text(error_message)

def main():
  """
  Funzione principale per l'avvio del bot.
  - Carica il token del bot dal file "token_bot".
  - Crea un Updater e un Dispatcher.
  - Registra i gestori per i comandi e i messaggi.
  - Avvia il bot e lo fa attendere i comandi degli utenti.
  """

  # Carica il token del bot dal file "token_bot"
  token_file = os.path.join(os.path.dirname(__file__), 'token_bot')
  with open(token_file, 'r') as f:
    TOKEN = f.read().strip()

  # Crea un Updater e un Dispatcher
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher

  # Registra i gestori per i comandi e i messaggi
  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

  # Avvia il bot e lo fa attendere i comandi degli utenti
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()
