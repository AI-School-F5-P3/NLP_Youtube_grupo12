import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
df = pd.read_csv('youtoxic_english_1000.csv')

# Visualizar las primeras filas
print(df.head())

# Información sobre el dataset
print(df.info())

# Estadísticas descriptivas
print(df.describe())

# Visualizar la distribución de mensajes tóxicos
plt.figure(figsize=(10, 6))
sns.countplot(x='IsToxic', data=df)
plt.title('Distribución de mensajes tóxicos')
plt.show()

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    # Convertir a minúsculas
    text = text.lower()

    # Eliminar caracteres especiales
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenización
    tokens = word_tokenize(text)

    # Eliminar stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    return ' '.join(tokens)


# Aplicar preprocesamiento
df['processed_text'] = df['Text'].apply(preprocess_text)