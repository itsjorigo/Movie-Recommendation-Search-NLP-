import streamlit as st
import requests

st.title("🎬 AI Movie Recommender")

query = st.text_input("Describe the kind of movie you want:")

if st.button("Search"):
    if query:
        response = requests.get(f"http://127.0.0.1:8000/search?query={query}")
        if response.status_code == 200:
            results = response.json()["movies"]
            st.subheader("🔍 Search Results:")
            for movie in results:
                st.write(f"**🎬 {movie['title']}**")
                st.write(f"📝 *{movie['overview']}*")
                st.write(f"🎭 Genres: {movie['genres']}")
                st.write("---")
        else:
            st.error("Error fetching data!")
