import os
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import faiss
import pandas as pd

# Load Data & Model
file_path = os.path.abspath("backend/cleaned_movies_2.csv")
print(f"Using file: {file_path}")

df = pd.read_csv(file_path)
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("movie_embeddings.index")

# Initialize FastAPI
app = FastAPI()

@app.get("/search")
def search_movies(query: str):
    # Convert query to embedding
    query_embedding = model.encode([query])
    
    # Search in FAISS
    _, indices = index.search(query_embedding, 5)  # Top 5 results

    # Get movie titles
    results = df.iloc[indices[0]][["title", "genres", "overview", "poster_path"]].to_dict(orient="records")
    return {"movies": results}

# Run API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)