# INSERT INTO diseases (name, treatment)
# VALUES ('Гастрит', 'пити багато рідини, відпочивати, уникати переохолодження');
#
# INSERT INTO symptoms (disease_id, symptom_text)
# VALUES
#
# (2, 'висока температура'),
# (2, 'головний біль'),
# (2, 'біль у горлі'),
# (2, 'кашель'),
# (2, 'ломота в тіліь');
#
# INSERT INTO medications (disease_id, medication_name)
# VALUES
# (2, 'Парацетамол'),
# (2, 'Відхаркувальні засоби'),
# (2, 'Ібупрофен');

index = input("Індекс: ")
while True:
    disease = input("Хвороба: ")
    treatment = input("Поради: ")
    symptoms = input("Симптоми (через кому ,): ")
    words = [word.strip() for word in symptoms.split(',') if word.strip()]
    medicaments = input("Медикаменти (через кому ,): ")
    words_medic = [word_medic.strip() for word_medic in medicaments.split(',') if word_medic.strip()]

    print("\nINSERT INTO diseases (name, treatment)")
    print(f"VALUES ('{disease}', '{treatment}');")
    print("")
    print("INSERT INTO symptoms (disease_id, symptom_text)")
    print("VALUES ")
    for i in range(len(words)):
        print(f"({index}, '{words[i]}'),")
    print("")
    print("INSERT INTO medications (disease_id, medication_name)")
    print("VALUES")
    for i in range(len(words_medic)):
        print(f"({index}, '{words_medic[i]}'),")

