import numpy as np
import pandas as pd

import ast
movies=pd.read_csv('tmdb_5000_movies.csv')
credits=pd.read_csv('tmdb_5000_credits.csv')
#print(movies.head(1))
movies=movies.merge(credits,on="title")
movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]
#print(movies.head(1))

#print(movies.isnull().sum()) to find missing values and then drop
movies.dropna(inplace=True)
#print(movies.isnull().sum()) 
#print(movies.duplicated().sum())# to find duplicate values

#preprocessing
movies.iloc[0].genres
# to covert data values to another format using function coz genres values in key-value pairs

def convert(obj):
    L=[]
    for i in  ast.literal_eval(obj): #to get list 
        L.append(i['name'])
    return L
movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)
def convert3(obj):
    L=[]
    count=0
    for i in  ast.literal_eval(obj): #to get list 
            if count!=3:  
                L.append(i['name'])
                count+=1
            else:
                 break
    return L
movies['cast']=movies['cast'].apply(convert3)

def fetch_director(obj):
    L=[]
    count=0
    for i in  ast.literal_eval(obj): #to get list 
            if i['job']=='Director': 
                L.append(i['name'])
                break
            
    return L
movies['crew']=movies['crew'].apply(fetch_director)
#print(movies.head(1))
movies['overview']=movies['overview'].apply(lambda x:x.split()) # it is to split column content to list...after that we can concanate to big paragraph

movies['genres']=movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords']=movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])#too remove space


movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

new_df=movies[['movie_id','title','tags']].copy()#creating df with neede columns
new_df.loc[:, 'tags']=new_df['tags'].apply(lambda x:" ".join(x))
new_df.loc[:, 'tags']=new_df['tags'].apply(lambda x:x.lower())

#text vectorization
#calculating similarities in both movies
#text --> vector convert for finding similarities
#finding closet vectors- vectors--> bags of words
#tag1+tag2...etc -->  large text then finding the frequncy 

#in 2d it select near vector

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()

#getting similar words
#to get words ['loved','loving','love']--->['love','love','love'] use nltk library

#to get 
import nltk
from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():#create list
       y.append(ps.stem(i)) #to get stem word
    return " ".join(y)    
new_df.loc[:, 'tags']=new_df['tags'].apply(stem) #now store love,loving,loved to love only

#after need to find the distance between nearest neighbour using cosine angle
from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vectors)
#it calculate distance with each movie and select closest movies

def recommend(movie):
    movie_index=new_df[new_df['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]  #this will sort ,index and value of movies and return 5 movies which is similar
    for i in movie_list:
        print(new_df.iloc[i[0]].title) 
        
recommend('Avatar')

import pickle
pickle.dump(new_df.to_dict(),open('movies_dict.pkl','wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))


