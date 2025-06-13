import sqlite3
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import configparser
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO)

# Завантаження конфігурації
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config['telegram']['token']

# Пошук хвороб
def find_diseases(symptoms_list):
    conn = sqlite3.connect('database/database.db')
    c = conn.cursor()

    placeholders = ', '.join('?' for _ in symptoms_list)
    query = f'''
        SELECT diseases.name, diseases.treatment,
               GROUP_CONCAT(DISTINCT medications.medication_name)
        FROM diseases
        JOIN symptoms ON diseases.id = symptoms.disease_id
        LEFT JOIN medications ON diseases.id = medications.disease_id
        WHERE symptoms.symptom_text IN ({placeholders})
        GROUP BY diseases.id
    '''
    c.execute(query, symptoms_list)
    results = c.fetchall()
    conn.close()
    return results

# Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    symptoms = [s.strip() for s in user_input.split(',')]
    results = find_diseases(symptoms)

    if results:
        response = "\n\n".join([
            f"🦠 Хвороба: {name}\n💊 Лікування: {treatment}\n📋 Ліки: {medications if medications else 'немає даних'}"
            for name, treatment, medications in results
        ])
    else:
        response = "😕 На жаль, не знайдено хвороб з такими симптомами."

    await update.message.reply_text(response)

# Обробка /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привіт! Напиши симптоми через кому — я підкажу можливі хвороби.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    if not os.path.exists("database/database.db"):
        print("⚠️ База даних не знайдена. Створи її перед запуском.")
    else:
        main()

