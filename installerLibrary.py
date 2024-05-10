import os
import subprocess

# Installa python-telegram-bot
subprocess.run(["pip", "install", "python-telegram-bot"])

# Installa telegram (facoltativo, potrebbe già essere installato come dipendenza di python-telegram-bot)
subprocess.run(["pip", "install", "telegram"])

# Installa pytube
subprocess.run(["pip", "install", "pytube"])

# Verifica che le librerie siano installate correttamente
try:
  import telegram
  from telegram.ext import Updater
  import pytube
  print("Librerie installate correttamente!")
except ImportError as e:
  print(f"Errore durante l'installazione delle librerie: {e}")
