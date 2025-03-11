import streamlit as st
import requests

st.title("🎬 AI Movie Recommender")

query = st.text_input("Describe the kind of movie you want:")

# Default image URL in case the poster is missing
default_poster_url = "https://drive-in-theatre.netlify.app/movieImages/default-movie.png"

# Function to check if the URL is accessible
def is_image_accessible(url):
    try:
        response = requests.head(url, timeout=3)  # Using HEAD request for fast checks
        return response.status_code == 200  # 200 means the image exists
    except requests.RequestException:
        return False  # If there's any exception, return False

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

                        if is_image_accessible(poster_url):
                            st.image(poster_url, width=150)  # Display the poster
                        else:
                            st.image(default_poster_url, width=150)

                    else:
                        st.image(poster_url, width=150)  # Set the width of the poster

                # Display movie details in the second column
                with col2:
                    st.write(f"**🎬 {movie['title']}**")
                    st.write(f"📝 *{movie['overview']}*")
                    st.write(f"🎭 Genres: {movie['genres']}")
                
                st.write("---")
        else:
            st.error("Error fetching data!")
