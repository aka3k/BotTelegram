import os
import subprocess

# Installa python-telegram-bot
subprocess.run(["pip", "install", "requests"])

# Installa pytube
subprocess.run(["pip", "install", "pytube"])

# Installa telebot
subprocess.run(["pip", "install", "telebot"])

# Verifica che le librerie siano installate correttamente
try:
  import telegram
  from telegram.ext import Updater
  import pytube
  print("Librerie installate correttamente!")
except ImportError as e:
  print(f"Errore durante l'installazione delle librerie: {e}")
