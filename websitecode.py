import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    if poster_path:
       return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
       return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]  #this will sort ,index and value of movies and return 5 movies which is similar
    recommend_movies=[]
    recommend_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from api
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
        
    return recommend_movies,recommend_movies_posters 
        

st.header('Movie Recommendation System')
movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
selected_movie_name=st.selectbox('Select one movie from list',movies['title'].values)

if st.button('Recommend'):
    
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    cols = st.columns(len(recommended_movie_names))

    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
