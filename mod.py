from imblearn.over_sampling import SMOTE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import re
import joblib
from gensim.models import KeyedVectors

# Preprocesar el texto
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)  # Eliminar caracteres no alfabéticos
    return text.strip()

# Cargar embeddings GloVe
def load_glove_model(file_path):
    print("Cargando modelo GloVe...")
    return KeyedVectors.load_word2vec_format(file_path, binary=False)

# Dataset
dataset_path = "youtube_toxic.csv"
data = pd.read_csv(dataset_path)

# Preprocesar texto
data['Processed_Text'] = data['Text'].apply(preprocess_text)

# Cargar GloVe y enriquecer texto
glove_path = "glove.6B.100d.word2vec.txt"
glove_model = load_glove_model(glove_path)

# Dividir en variables independientes y dependientes
X = data['Processed_Text']
y = data['IsToxic']

# Vectorización TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=10000, stop_words="english")

# Sobremuestreo con SMOTE
smote = SMOTE(random_state=42)
X_vectorized = tfidf_vectorizer.fit_transform(X)
X_resampled, y_resampled = smote.fit_resample(X_vectorized, y)

# Modelo Ajustado XGBoost
xgb_model = XGBClassifier(
    scale_pos_weight=1.6,
    n_estimators=800,
    learning_rate=0.12,
    max_depth=5,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    eval_metric="logloss"
)

# Crear pipeline
pipeline = Pipeline([
    ('tfidf', tfidf_vectorizer),
    ('model', xgb_model)
])

# Dividir el conjunto de datos para evaluación explícita de sobreajuste
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Entrenar modelo en conjunto de entrenamiento
pipeline.fit(X_train, y_train)

# Evaluar en conjunto de entrenamiento
train_predictions = pipeline.predict(X_train)
train_accuracy = accuracy_score(y_train, train_predictions)

# Evaluar en conjunto de prueba
test_predictions = pipeline.predict(X_test)
test_accuracy = accuracy_score(y_test, test_predictions)

# Validación cruzada
stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X_resampled, y_resampled, cv=stratified_kfold, scoring="accuracy")
cv_mean_accuracy = cv_scores.mean()

# Cálculo del overfitting
overfitting = train_accuracy - cv_mean_accuracy

# Resultados
print(f"Accuracy del modelo (conjunto de entrenamiento): {train_accuracy:.4f}")
print(f"Validación cruzada (accuracy promedio): {cv_mean_accuracy:.4f}")
print(f"Overfitting: {overfitting:.4f}")

# Reporte del conjunto de prueba
test_report = classification_report(y_test, test_predictions)
test_conf_matrix = confusion_matrix(y_test, test_predictions)

print("Reporte de Clasificación en conjunto de prueba:\n", test_report)
print("Matriz de Confusión en conjunto de prueba:\n", test_conf_matrix)

# Guardar el pipeline
joblib.dump(pipeline, "pipeline_with_overfitting_analysis.joblib")
print("Pipeline guardado como 'pipeline_with_overfitting_analysis.joblib'")
