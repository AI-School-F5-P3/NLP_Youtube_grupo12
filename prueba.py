import joblib

# Cargar el modelo
pipeline = joblib.load("final_pipeline_glove_optimized.joblib")

# Palabras y frases para evaluar
test_phrases = [
    "I hate you", "You are amazing", "This is terrible", "Fantastic effort",
    "Garbage work", "You are the best", "Shut your mouth", "Keep shining",
    "I am proud of you", "You are a fool", "Such a great achievement",
    "Nobody likes you", "Go to hell", "Thank you for your help",
    "What a wonderful day", "You are so dumb", "Kind and gentle words",
    "Filthy behavior", "Stop being so rude", "This is awesome",
    "Absolutely ridiculous", "You are disgusting", "I am so happy for you",
    "Stay positive", "What a pathetic idea", "Learn some manners",
    "I can't stand you", "Brilliant job", "Terrible mistake",
    "You're an inspiration", "Awful comments", "This is delightful",
    "You always ruin everything", "Horrible attitude", "Such a nasty remark",
    "So grateful for your support", "You're such a loser", "Thank you so much",
    "Shut up and listen", "What a joke", "Incredible performance",
    "Racist behavior is unacceptable", "Misogynistic comment",
    "I appreciate your kindness", "Completely unacceptable",
    "Fantastic teamwork", "Such offensive language", "What a mess",
    "You are a disgrace", "Pure hatred"
]

# Realizar predicciones
predictions = pipeline.predict(test_phrases)

# Mostrar resultados
for phrase, prediction in zip(test_phrases, predictions):
    result = "Tóxico" if prediction == 1 else "No tóxico"
    print(f"Comentario: '{phrase}' --> {result}")
