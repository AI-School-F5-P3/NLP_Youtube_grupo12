import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import classification_report, f1_score
from sklearn.pipeline import Pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

# Descargar recursos de NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Función de preprocesamiento
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

# Cargar los datos
df = pd.read_csv('youtoxic_english_1000.csv')

# Aplicar preprocesamiento
df['processed_text'] = df['Text'].apply(preprocess_text)

# Preparar características (X) y etiquetas (y)
X = df['processed_text']
y = df['IsToxic']

# Dividir en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear el pipeline con Voting Classifier
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000)),
    ('clf', VotingClassifier(estimators=[
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
        ('lr', LogisticRegression(random_state=42)),
        ('svm', SVC(probability=True, random_state=42))
    ], voting='soft'))
])

# Entrenar el modelo
pipeline.fit(X_train, y_train)

# Evaluar en conjunto de entrenamiento
y_train_pred = pipeline.predict(X_train)
train_f1 = f1_score(y_train, y_train_pred)

# Evaluar en conjunto de prueba
y_test_pred = pipeline.predict(X_test)
test_f1 = f1_score(y_test, y_test_pred)

# Calcular overfitting
overfitting = train_f1 - test_f1

print("F1-score en entrenamiento:", train_f1)
print("F1-score en prueba:", test_f1)
print("Overfitting (diferencia):", overfitting)
print("\nInforme de clasificación en conjunto de prueba:")
print(classification_report(y_test, y_test_pred))

# Función para clasificar nuevos comentarios
def classify_comment(comment):
    processed = preprocess_text(comment)
    prediction = pipeline.predict([processed])
    return "Tóxico" if prediction[0] else "No tóxico"

# Ejemplo de uso
print("\nEjemplos de clasificación:")
print(classify_comment("You are an idiot!"))
print(classify_comment("Have a nice day!"))