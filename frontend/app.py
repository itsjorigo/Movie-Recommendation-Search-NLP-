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
                # Create two columns: one for the image and one for the text
                col1, col2 = st.columns([1, 3])  # You can adjust the ratio of columns

                # Display movie poster in the first column
                with col1:
                    if movie['poster_path']:
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                        st.image(poster_url, width=150)  # Set the width of the poster

                # Display movie details in the second column
                with col2:
                    st.write(f"**🎬 {movie['title']}**")
                    st.write(f"📝 *{movie['overview']}*")
                    st.write(f"🎭 Genres: {movie['genres']}")
                
                st.write("---")
        else:
            st.error("Error fetching data!")
