import pickle
import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ---------------------------- Styling only ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=DM+Sans:wght@400;500;600&display=swap');

:root {
  --bg: #14152a;
  --surface: #1e2040;
  --border: #343867;
  --text: #eceaf6;
  --muted: #9a9dc4;
  --accent: #f4b942;
  --radius: 14px;
}

html, body, .stApp, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: radial-gradient(1200px 600px at 50% -10%, #23265a 0%, var(--bg) 60%); color: var(--text); }

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 1180px; padding-top: 3rem; padding-bottom: 4rem; }

/* Header */
h2, [data-testid="stHeadingWithActionElements"] h2 {
  font-family: 'Bricolage Grotesque', sans-serif !important;
  font-weight: 800 !important; font-size: clamp(2.2rem, 5vw, 3.4rem) !important;
  letter-spacing: -0.02em; line-height: 1.05; color: var(--text) !important;
  padding-bottom: 1.2rem !important;
}

/* Select box */
label[data-testid="stWidgetLabel"] p { color: var(--muted) !important; font-weight: 500; }
div[data-baseweb="select"] > div {
  background: var(--surface) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; min-height: 3.2rem; color: var(--text) !important;
}
div[data-baseweb="select"] > div:focus-within { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(244,185,66,.22); }
div[data-baseweb="select"] * { color: var(--text) !important; }
div[data-baseweb="popover"] ul { background: var(--surface) !important; }

/* Button */
[data-testid="stButton"] button {
  background: var(--accent); color: #1a1a2e; font-weight: 600; font-size: 1rem;
  border: none; border-radius: var(--radius); padding: .65rem 1.6rem;
  transition: transform .15s ease, box-shadow .15s ease;
}
[data-testid="stButton"] button:hover { background: #ffc75a; color: #1a1a2e; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(244,185,66,.3); }
[data-testid="stButton"] button:focus-visible { outline: 3px solid rgba(244,185,66,.5); outline-offset: 2px; }
[data-testid="stButton"] button:active { transform: translateY(0); }

/* Results */
[data-testid="stHorizontalBlock"] { margin-top: 1.6rem; }
/* Force all 5 columns to be exactly equal width so no poster can grow larger */
[data-testid="stColumn"], [data-testid="column"] { flex: 1 1 0 !important; width: 0 !important; min-width: 0 !important; }
[data-testid="stText"], [data-testid="stText"] * {
  font-family: 'DM Sans', sans-serif !important; font-weight: 600; font-size: 1rem;
  line-height: 1.3; color: var(--text) !important; white-space: normal !important;
  min-height: 2.6em; display: flex; align-items: flex-end;
}
[data-testid="stImage"] { width: 100% !important; }
[data-testid="stImage"] img {
  width: 100% !important; aspect-ratio: 2 / 3; object-fit: cover; display: block;
  border-radius: var(--radius); box-shadow: 0 10px 28px rgba(5,6,20,.55);
  transition: transform .2s ease, box-shadow .2s ease;
}
[data-testid="stImage"] img:hover { transform: translateY(-5px); box-shadow: 0 16px 34px rgba(5,6,20,.7), 0 0 0 2px var(--accent); }

@media (prefers-reduced-motion: reduce) {
  [data-testid="stImage"] img, [data-testid="stButton"] button { transition: none; }
}
</style>
""", unsafe_allow_html=True)

# ---------------------------- Original logic ----------------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    index = movies[movies['title_x'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title_x)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

# Load dictionary and convert back to DataFrame
movies_dict = pickle.load(open('model/data_set.pkl', 'rb'))
movies = pd.DataFrame(movies_dict).reset_index(drop=True)

similarity = pickle.load(open('model/similarity_set.pkl', 'rb'))

movie_list = movies['title_x'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5, gap="large")
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])