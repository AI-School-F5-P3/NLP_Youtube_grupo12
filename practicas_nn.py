# Importar las bibliotecas necesarias
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from transformers import get_linear_schedule_with_warmup
import torch
from torch.utils.data import DataLoader, TensorDataset
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de semilla para reproducibilidad
torch.manual_seed(42)
np.random.seed(42)

# Cargar el dataset
df = pd.read_csv('youtoxic_english_1000.csv')

# Preparar los datos
X = df['Text']
y = df['IsToxic'].astype(int)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configuración de hiperparámetros
MAX_LENGTH = 512
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
EPOCHS = 5

# Tokenización con DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

def tokenize_texts(texts, tokenizer, max_length=MAX_LENGTH):
    return tokenizer(
        list(texts),
        max_length=max_length,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

# Tokenizar los datos
train_encodings = tokenize_texts(X_train, tokenizer)
test_encodings = tokenize_texts(X_test, tokenizer)

# Crear datasets para PyTorch
train_dataset = TensorDataset(
    train_encodings['input_ids'], 
    train_encodings['attention_mask'], 
    torch.tensor(y_train.values, dtype=torch.long)
)
test_dataset = TensorDataset(
    test_encodings['input_ids'], 
    test_encodings['attention_mask'], 
    torch.tensor(y_test.values, dtype=torch.long)
)

# Crear DataLoader para entrenamiento y prueba
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE)

# Configuración del dispositivo
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Usando dispositivo: {device}")

# Cargar modelo DistilBERT
model = DistilBertForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', 
    num_labels=2
).to(device)

# Configuración del optimizador con schedule
optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
total_steps = len(train_loader) * EPOCHS
scheduler = get_linear_schedule_with_warmup(
    optimizer, 
    num_warmup_steps=0, 
    num_training_steps=total_steps
)

# Función de entrenamiento mejorada
def train_model(model, train_loader, optimizer, scheduler, device, epochs):
    model.train()
    training_stats = []

    for epoch in range(epochs):
        total_train_loss = 0
        
        progress_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{epochs}', leave=True)
        
        for batch in progress_bar:
            input_ids, attention_mask, labels = [b.to(device) for b in batch]

            model.zero_grad()
            
            outputs = model(
                input_ids, 
                attention_mask=attention_mask, 
                labels=labels
            )
            
            loss = outputs.loss
            total_train_loss += loss.item()
            
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            
            optimizer.step()
            scheduler.step()
            
            progress_bar.set_postfix({'loss': loss.item()})
        
        avg_train_loss = total_train_loss / len(train_loader)
        training_stats.append({
            'epoch': epoch + 1,
            'avg_train_loss': avg_train_loss
        })
    
    return training_stats

# Entrenar el modelo
training_stats = train_model(model, train_loader, optimizer, scheduler, device, EPOCHS)

# Evaluar el modelo
def evaluate_model(model, test_loader, device):
    model.eval()
    y_preds = []
    y_true = []

    with torch.no_grad():
        for batch in tqdm(test_loader, desc="Evaluación"):
            input_ids, attention_mask, labels = [b.to(device) for b in batch]
            
            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            
            y_preds.extend(torch.argmax(logits, axis=1).cpu().numpy())
            y_true.extend(labels.cpu().numpy())

    return y_true, y_preds

# Obtener predicciones y métricas
y_true, y_preds = evaluate_model(model, test_loader, device)

# Reporte de clasificación
print("\nInforme de clasificación en prueba:")
print(classification_report(y_true, y_preds))

# Matriz de confusión
cm = confusion_matrix(y_true, y_preds)
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Confusión')
plt.ylabel('Etiquetas Reales')
plt.xlabel('Predicciones')
plt.tight_layout()
plt.savefig('confusion_matrix.png')

# Guardar modelo y tokenizador
model_save_path = 'C:/Users/busin/Desktop/NLP_Youtube_grupo12/modelo_toxicidad/'
model.save_pretrained(model_save_path)
tokenizer.save_pretrained(model_save_path)

# Prueba con ejemplos
test_sentences = [
    "I love how diverse and multicultural our community is!",
    "You're stupid and worthless because of your race",
    "Everyone deserves to be treated with respect and dignity",
    "All [ethnic group] should be banned from this country!",
    "Had a great time learning about different cultures today"
]

# Tokenizar y predecir ejemplos
def predict_sentences(sentences, model, tokenizer, device):
    inputs = tokenizer(
        sentences,
        max_length=MAX_LENGTH,
        padding=True,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=1).cpu().numpy()

    return predictions

# Obtener y mostrar predicciones
predictions = predict_sentences(test_sentences, model, tokenizer, device)

print("\nPredicciones de ejemplo:")
for sentence, pred in zip(test_sentences, predictions):
    label = "HATE SPEECH" if pred == 1 else "NO HATE SPEECH"
    print(f"\nTexto: {sentence}")
    print(f"Predicción: {label}")