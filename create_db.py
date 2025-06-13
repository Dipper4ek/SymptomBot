import sqlite3

conn = sqlite3.connect("database/database.db")
c = conn.cursor()

# Створення таблиць
c.execute('''
CREATE TABLE IF NOT EXISTS diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    treatment TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS symptoms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_id INTEGER,
    symptom_text TEXT,
    FOREIGN KEY (disease_id) REFERENCES diseases(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS medications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease_id INTEGER,
    medication_name TEXT,
    FOREIGN KEY (disease_id) REFERENCES diseases(id)
)
''')

# Приклад вставки даних
c.execute("INSERT INTO diseases (name, treatment) VALUES (?, ?)", ("Грип", "Пити воду, відпочивати, жарознижувальні"))
disease_id = c.lastrowid

symptoms = ['жар', 'головний біль', 'кашель', 'слабкість']
for s in symptoms:
    c.execute("INSERT INTO symptoms (disease_id, symptom_text) VALUES (?, ?)", (disease_id, s))

meds = ['Парацетамол', 'Ібупрофен']
for m in meds:
    c.execute("INSERT INTO medications (disease_id, medication_name) VALUES (?, ?)", (disease_id, m))

conn.commit()
conn.close()

print("✅ Базу даних створено та заповнено.")

