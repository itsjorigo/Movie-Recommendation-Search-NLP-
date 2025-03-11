from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd
import numpy as np

# Load cleaned movie data
df = pd.read_csv("cleaned_movies.csv")

# Load pre-trained Sentence-BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings for movie descriptions
embeddings = model.encode(df["overview"].tolist(), convert_to_numpy=True)

# Save embeddings using FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])  # L2 distance index
index.add(embeddings)  # Add embeddings to FAISS index

# Save FAISS index
faiss.write_index(index, "movie_embeddings.index")

print("Movie embeddings generated & stored!")

