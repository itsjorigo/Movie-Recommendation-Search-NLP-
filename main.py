import subprocess
import threading
import uvicorn
import streamlit.web.bootstrap
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

# Function to run FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Function to run Streamlit
def run_streamlit():
    streamlit.web.bootstrap.run("frontend.app")

if __name__ == "__main__":
    # Run FastAPI in one thread
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    # Run Streamlit in another thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()

    fastapi_thread.join()
    streamlit_thread.join()
