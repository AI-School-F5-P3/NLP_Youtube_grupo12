from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors

# Ruta del archivo GloVe original
glove_path = "glove.6B.100d.txt"

# Archivo convertido a formato Word2Vec
word2vec_output_file = "glove.6B.100d.word2vec.txt"

# Convertir el archivo
glove2word2vec(glove_path, word2vec_output_file)

# Cargar el modelo convertido
glove_model = KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)
print("Modelo GloVe cargado correctamente.")
