from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
import re
import joblib

# Preprocesar el texto
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)  # Eliminar caracteres no alfabéticos
    return text

# Diccionario Extenso de Palabras Positivas (No tóxicas)
positive_exclusions = {
    "happy", "great", "wonderful", "love", "nice", "amazing", "kind", "joyful", "pleasant", "delightful",
    "cheerful", "bright", "peaceful", "fantastic", "awesome", "excellent", "perfect", "beautiful", "grateful",
    "friendly", "sweet", "gentle", "elegant", "charming", "compassionate", "thoughtful", "caring", "considerate",
    "generous", "affectionate", "enthusiastic", "encouraging", "supportive", "inspiring", "uplifting", "brilliant",
    "talented", "passionate", "optimistic", "humble", "respectful", "polite", "honest", "truthful", "trustworthy",
    "loyal", "dedicated", "dependable", "sincere", "hopeful", "motivated", "ambitious", "hardworking", "persistent",
    "resilient", "faithful", "spiritual", "innovative", "creative", "resourceful", "flexible", "adaptable", 
    "cooperative", "collaborative", "team-player", "hard-worker", "selfless", "altruistic", "charitable", 
    "philanthropic", "diligent", "kindhearted", "considerate", "sympathetic", "forgiving", "gracious", "tolerant",
    "respectable", "moral", "ethical", "principled", "trustful", "reliable", "steady", "fair", "justice-seeking",
    "peace-seeking", "lovely", "radiant", "energetic", "vibrant", "blissful", "harmonious", "balanced", "amazing",
    "adorable", "marvelous", "incredible", "stunning", "extraordinary", "inspiring", "heartwarming", "kindness"
}

# Diccionario Extenso de Sinónimos Tóxicos
toxic_dictionary = {
    "toxic": [
        "harmful", "poisonous", "malicious", "vicious", "hostile", "evil", "sinister", "damaging", "nasty",
        "offensive", "rude", "insulting", "abusive", "hateful", "aggressive", "violent", "cruel", "antagonistic",
        "mean", "horrible", "disgusting", "filthy", "vile", "repulsive", "derogatory", "demeaning", "oppressive",
        "despicable", "spiteful", "venomous", "horrendous", "intimidating", "bullying", "threatening", "harassing"
    ],
    "racist": [
        "racist", "nigger", "nigga", "blackface", "slave", "cracker", "coon", "monkey", "ape", "sambo", "lynch",
        "segregation", "supremacist", "xenophobic", "anti-black", "mudskin", "darkie", "neo-nazi", "anti-semitic"
    ],
    "sexist": [
        "sexist", "misogynist", "chauvinist", "anti-women", "patriarchal", "derogatory", "demeaning", "objectifying",
        "anti-feminist", "prejudiced", "biased", "macho", "oppressive", "stereotypical", "androcentric"
    ],
    "obscene": [
        "obscene", "vulgar", "lewd", "crude", "profane", "indecent", "offensive", "pornographic", "dirty", "filthy",
        "salacious", "lascivious", "improper", "gross", "disgusting", "nasty", "shocking", "repugnant", "uncouth"
    ],
    "hatespeech": [
        "hateful", "bigoted", "derogatory", "demeaning", "anti-gay", "anti-black", "anti-muslim", "anti-jewish",
        "neo-nazi", "white-supremacist", "anti-semitic", "intolerant", "lynch", "klan", "oppressive", "anti-lgbt"
    ]
}

# Enriquecer el texto con sinónimos, excluyendo palabras positivas
def enrich_text_with_synonyms(text, synonym_dict, exclusions=set()):
    words = text.split()
    enriched_text = []
    for word in words:
        if word in exclusions:
            enriched_text.append(word)
        elif word in synonym_dict:
            enriched_text.extend(synonym_dict[word])
        else:
            enriched_text.append(word)
    return " ".join(enriched_text)

# Cargar dataset
dataset_path = "youtoxic_english_1000.csv"  # Cambia la ruta al archivo
data = pd.read_csv(dataset_path)

# Preprocesar y enriquecer el texto
data['Processed_Text'] = data['Text'].apply(preprocess_text)
data['Enriched_Text'] = data['Processed_Text'].apply(
    lambda x: enrich_text_with_synonyms(x, toxic_dictionary, positive_exclusions)
)

# Dividir en variables independientes y dependientes
X = data['Enriched_Text']
y = data['IsToxic']

# Vectorización TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")

# Sobremuestrear con SMOTE
smote = SMOTE(random_state=42)
X_vectorized = tfidf_vectorizer.fit_transform(X)
X_resampled, y_resampled = smote.fit_resample(X_vectorized, y)

# Crear el modelo con ajustes
xgb_model = XGBClassifier(
    scale_pos_weight=1.,  # Ajustado para balancear mejor las clases
    n_estimators=600,  # Aumentar árboles para mejorar precisión
    learning_rate=0.05,  # Disminuir la tasa de aprendizaje
    max_depth=5,  # Ajustar para capturar patrones más complejos
    reg_lambda=2,  # Regularización moderada
    reg_alpha=1,  # Regularización ligera
    random_state=42,
    eval_metric="logloss"
)

# Crear pipeline
pipeline = Pipeline([
    ('tfidf', tfidf_vectorizer),
    ('model', xgb_model)
])

# Validación cruzada estratificada
stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X, y, cv=stratified_kfold, scoring="accuracy")

# Entrenar el pipeline con todos los datos
pipeline.fit(X, y)

# Evaluar el modelo en el conjunto de prueba
y_pred = pipeline.predict(X)

# Mostrar métricas
accuracy = accuracy_score(y, y_pred)
classification_rep = classification_report(y, y_pred)
conf_matrix = confusion_matrix(y, y_pred)

print(f"Accuracy del modelo: {accuracy:.4f}")
print(f"Validación cruzada (accuracy promedio): {cv_scores.mean():.4f}")
print("Reporte de Clasificación:\n", classification_rep)
print("Matriz de Confusión:\n", conf_matrix)

# Guardar el pipeline completo
joblib.dump(pipeline, "ensemble_model.joblib")
print("Pipeline guardado como 'ensemble_pipeline.joblib'")
