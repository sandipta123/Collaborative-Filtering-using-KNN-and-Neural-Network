# -*- coding: utf-8 -*-
"""mlda2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fvSBKg5ySYuuqi7Up7F36xLZt7Qvk4Jb

#**Collaborative Filtering using knn**
"""

import pandas as pd
import numpy as np
from collections import Counter

df1=pd.read_csv('/content/movies.csv',usecols=['movieId','title'])
df1.head()

df=pd.read_csv('/content/ratings.csv',usecols=['userId','movieId','rating'])
df.head()

a=df.groupby(['movieId']).count()['userId']
a

a.values

"""**calculate nearest neighbour**

Using NearestNeighbors() to calculate the distance between movies using cosine similarity and find the most similar movies for each movie.
"""

from sklearn.neighbors import NearestNeighbors
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)
distances, indices = knn.kneighbors(df.values, n_neighbors=3)

"""The parameter for the number of the nearest neighbors is set to be 3."""

indices

"""indices=nearest movies to each movie. for example [0,1,561] means movies0 is closest to itself , then to 1 and then to 561"""

distances

"""distances= distance between movies

**Predict a Rating for a Movie by a User**
"""

for title in df.index:

  index_user_likes = df.index.tolist().index(title) # get an index for a movie
  sim_movies = indices[index_user_likes].tolist() # make list for similar movies
  movie_distances = distances[index_user_likes].tolist() # the list for distances of similar movies
  id_movie = sim_movies.index(index_user_likes) # get the position of the movie itself in indices and distances

  print('Similar Movies to '+str(df.index[index_user_likes])+':\n')


  sim_movies.remove(index_user_likes) # remove the movie itself in indices
  movie_distances.pop(id_movie) # remove the movie itself in distances

  j = 1
  
  for i in sim_movies:
    print(str(j)+': '+str(df.index[i])+', the distance with '+str(title)+': '+str(movie_distances[j-1]))
    j = j + 1
      
  print('\n')

"""##**Recommend Similar Movies to a Selected Movie**

Using the algorithm above, we can make a recommender for the similar movies to a selected movie by users.
"""

def recommend_movie(title):

  index_user_likes = df.index.tolist().index(title) # get an index for a movie
  sim_movies = indices[index_user_likes].tolist() # make list for similar movies
  movie_distances = distances[index_user_likes].tolist() # the list for distances of similar movies
  id_movie = sim_movies.index(index_user_likes) # get the position of the movie itself in indices and distances

  print('Similar Movies to '+str(df.index[index_user_likes])+': \n')

  sim_movies.remove(index_user_likes) # remove the movie itself in indices
  movie_distances.pop(id_movie) # remove the movie itself in distances

  j = 1
    
  for i in sim_movies:
    print(str(j)+': '+str(df.index[i])+', the distance with '+str(title)+': '+str(movie_distances[j-1]))
    j = j + 1

recommend_movie(1)
recommend_movie(100014)
recommend_movie(0)

"""##**Recommend Movies for a Selected User**"""

index_for_movie = df.index.tolist().index(0) # it returns 0
sim_movies = indices[index_for_movie].tolist() # make list for similar movies
movie_distances = distances[index_for_movie].tolist() # the list for distances of similar movies
id_movie = sim_movies.index(index_for_movie) # get the position of the movie itself in indices and distances
sim_movies.remove(index_for_movie) # remove the movie itself in indices
movie_distances.pop(id_movie) # remove the movie itself in distances

print('The Nearest Movies to movie_0:', sim_movies)
print('The Distance from movie_0:', movie_distances)

"""Predict a Rating (when rating is not given for a particular movie)
Algorithm: predicted rating for a movie is the weighted average of ratings for similar movies.

Build a Recommender
"""

ratings=pd.merge(df,df1,how='inner', on='movieId')
ratings.head()

df = ratings.pivot_table(index='title',columns='userId',values='rating').fillna(0)
df1 = df.copy()

def recommend_movies(user, num_recommended_movies):

  print('The list of the Movies {} Has Watched \n'.format(user))

  for m in df[df[user] > 0][user].index.tolist():
    print(m)
  
  print('\n')

  recommended_movies = []

  for m in df[df[user] == 0].index.tolist():

    index_df = df.index.tolist().index(m)
    predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
    recommended_movies.append((m, predicted_rating))

  sorted_rm = sorted(recommended_movies, key=lambda x:x[1], reverse=True)
  
  print('The list of the Recommended Movies \n')
  rank = 1
  for recommended_movie in sorted_rm[:num_recommended_movies]:
    
    print('{}: {} - predicted rating:{}'.format(rank, recommended_movie[0], recommended_movie[1]))
    rank = rank + 1

def movie_recommender(user, num_neighbors, num_recommendation):
  
  number_neighbors = num_neighbors

  knn = NearestNeighbors(metric='cosine', algorithm='brute')
  knn.fit(df.values)
  distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)

  user_index = df.columns.tolist().index(user)

  for m,t in list(enumerate(df.index)):
    if df.iloc[m, user_index] == 0:
      sim_movies = indices[m].tolist()
      movie_distances = distances[m].tolist()
    
      if m in sim_movies:
        id_movie = sim_movies.index(m)
        sim_movies.remove(m)
        movie_distances.pop(id_movie) 

      else:
        sim_movies = sim_movies[:num_neighbors-1]
        movie_distances = movie_distances[:num_neighbors-1]
           
      movie_similarity = [1-x for x in movie_distances]
      movie_similarity_copy = movie_similarity.copy()
      nominator = 0

      for s in range(0, len(movie_similarity)):
        if df.iloc[sim_movies[s], user_index] == 0:
          if len(movie_similarity_copy) == (number_neighbors - 1):
            movie_similarity_copy.pop(s)
          
          else:
            movie_similarity_copy.pop(s-(len(movie_similarity)-len(movie_similarity_copy)))
            
        else:
          nominator = nominator + movie_similarity[s]*df.iloc[sim_movies[s],user_index]
          
      if len(movie_similarity_copy) > 0:
        if sum(movie_similarity_copy) > 0:
          predicted_r = nominator/sum(movie_similarity_copy)
        
        else:
          predicted_r = 0

      else:
        predicted_r = 0
        
      df1.iloc[m,user_index] = predicted_r
  recommend_movies(user,num_recommendation)

movie_recommender(15, 10, 10)

movie_recommender(4, 10, 10)

movie_recommender(2, 10, 10)

"""#**Neural Collaborative Filtering(NCF)**"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ratings=pd.read_csv('/content/ratings.csv',usecols=['userId','movieId','rating'])
ratings.head()

n_users, n_movies = len(ratings.userId.unique()), len(ratings.movieId.unique())
f'The dataset includes {len(ratings)} ratings by {n_users} unique users for {n_movies} unique movies'

train_df=pd.read_csv('/content/train12.csv',usecols=['userId','movieId','rating'])
train_df.head()

cnt_1=0
cnt_2=0
cnt_3=0
cnt_4=0
cnt_5=0
for x in train_df.iterrows():
    if x[1]['rating']==1:
        cnt_1 += 1
    elif x[1]['rating']==2:
        cnt_2 += 1
    elif x[1]['rating']==3:
        cnt_3 += 1
    elif x[1]['rating']==4:
        cnt_4 += 1
    elif x[1]['rating']==5:
        cnt_5 += 1

"""Distribution of Ratings in the Dataset"""

import matplotlib.pyplot as plt
import numpy as np
label = [1,2,3,4,5]
no_ratings = [cnt_1,cnt_2,cnt_3,cnt_4,cnt_5]
index = np.arange(len(label))
plt.bar(index, no_ratings)
plt.xlabel('Rating_value', fontsize=18)
plt.ylabel('No of Ratings', fontsize=18)
plt.xticks(index, label, fontsize=10, rotation=30)
# plt.title('Market Share for Each Genre 1995-2017')
plt.show()

len(train_df.movieId.unique())

n_users, n_movies = len(train_df.userId.unique()), len(train_df.movieId.unique())
f'The dataset includes {len(train_df)} ratings by {n_users} unique users for {n_movies} unique movies'

"""Matrix Factorization with Neural Networks"""

from keras.models import Sequential, Model
from keras.layers import Embedding, Flatten, Dense, Dropout, concatenate, multiply, Input
from tensorflow.keras.optimizers import Adam

from sklearn.datasets import load_iris
from sklearn import preprocessing

dim_embedding_user = 40
dim_embedding_movie = 40
#book embedding
movie_input = Input(shape=[1],name = 'Movie')
# movie_input = preprocessing.scale(movie_input)
movie_embedding = Embedding(n_movies+1,dim_embedding_movie,name='Movie-Embedding')(movie_input)
movie_vec = Flatten(name='movie_flatten')(movie_embedding)
movie_vec = Dropout(0.2)(movie_vec)
#user embedding
user_input = Input(shape=[1],name='User')
# user_input = preprocessing.scale(user_input)
user_embedding = Embedding(n_users+1,dim_embedding_user,name = 'User-Embedding')(user_input)
user_vec = Flatten(name='user_flatten')(user_embedding)
user_vec = Dropout(0.2)(user_vec)
#concatenate flattened values
concat = concatenate([movie_vec,user_vec])
concat_dropout = Dropout(0.2)(concat)
#dense layer
dense = Dense(20,name='Fully-Connected1',activation='relu')(concat)
result = Dense(1,activation='relu',name='Activation')(dense)
#define model
model = Model([user_input,movie_input],result)
#show model summary
model.summary()

from sklearn.datasets import load_iris
from sklearn import preprocessing
x_user = preprocessing.scale(train_df['userId'])

train_df['rating'].size

opt_adam = Adam(lr = 2e-3)

## compile model
model.compile(optimizer= opt_adam, loss= ['mse'], metrics=['mean_absolute_error'])

## fit model
history_tabular = model.fit([train_df['userId'],train_df['movieId']],
                                    train_df['rating'],
                                    batch_size = 256,
                                    validation_split = 0.1,
                                    epochs = 10,
                                    verbose = 1)

pd.DataFrame(history_tabular.history)

test_df = pd.read_csv("/content/test12.csv")
test_df.head()

print(model.metrics_names)
#storing testing ratings
actual=train_df.iloc[:, 2:3]
model.evaluate(x=[test_df['userId'],test_df['movieId']],y=test_df['rating'],verbose=0)

import numpy as np
pr = list(model.predict(x=[test_df['userId'],test_df['movieId']]))
predicted_ratings = list()
for i in range (0,len(pr)):
  predicted_ratings.append(pr[i][0])
#predicted_ratings = np.round_(predicted_ratings)
#print(predicted_ratings[:20])

userId = np.array(test_df['userId'])
movieId = np.array(test_df['movieId'])
actual_ratings = np.array(test_df['rating'])

# importing the required module
import matplotlib.pyplot as plt

plt.scatter(movieId[:500],actual_ratings[:500],label= "stars", color= "blue", marker= "*")
plt.scatter(movieId[:500],predicted_ratings[:500],label= "stars", color= "orange", marker= "*")
plt.title('Predicted vs Actual w.r.t MovieID')
plt.ylabel('ratings')
plt.xlabel('movieId')
plt.legend(['actual', 'predicted'], loc='upper left')
plt.show()

plt.scatter(userId[:500],actual_ratings[:500],label= "stars", color= "blue", marker= "*")
plt.scatter(userId[:500],predicted_ratings[:500],label= "stars", color= "orange", marker= "*")
plt.title('Predicted vs Actual w.r.t UserID')
plt.ylabel('ratings')
plt.xlabel('userId')
plt.legend(['actual', 'predicted'], loc='upper left')
plt.show()

comparision = pd.DataFrame(list(zip(actual_ratings, predicted_ratings)), index = list(movieId),columns =['Actual', 'Predicted'])
comparision

#evaluates on test set
from sklearn.metrics import mean_squared_error,r2_score
def score_on_test_set():
#user_movie_pairs = zip(valid_df[???movieId???], valid_df[???userId???])
  predicted_ratings = np.array(comparision[['Predicted']])
  true_ratings = np.array(comparision[['Actual']])
  score = np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
  return score
test_set_score = score_on_test_set()
print(test_set_score)
print(r2_score(actual_ratings, predicted_ratings))

import math

s=c=0
for i in range (0,len(actual_ratings)):
  if(predicted_ratings[i]>=4.82):
    s = s + ((actual_ratings[i]-predicted_ratings[i])**2)
    c+=1
s = math.sqrt(float(s/c))
print(s)
print(c)

"""Tabular Data Method"""

dim_embedding_user = 50
dim_embedding_movie = 50
#movie embedding
movie_input = Input(shape=[1],name='Movie')
movie_embedding = Embedding(n_movies+1,dim_embedding_movie,name='Movie-Embedding')(movie_input)
movie_vec = Flatten(name='Movie-Flatten')(movie_embedding)
movie_vec = Dropout(0.2)(movie_vec)
#user embedding
user_input = Input(shape=[1],name = 'User')
user_embedding = Embedding(n_users+1,dim_embedding_user,name='User-Embedding')(user_input)
user_vec = Flatten(name='User-Flatten')(user_embedding)
user_vec = Dropout(0.2)(user_vec)
concat = concatenate([movie_vec,user_vec])
concat_dropout = Dropout(0.2)(concat)
dense_1 = Dense(20,name='Fully-Connected1',activation ='relu')(concat)
result = Dense(1,activation='relu',name='Activation')(dense_1)
model_tabular = Model([user_input,movie_input],result)
model_tabular.summary()

opt_adam = Adam(lr = 0.002)

## compile model
model_tabular.compile(optimizer= opt_adam, loss= ['mse'], metrics=['mean_absolute_error'])

history_tabular1 = model_tabular.fit([train_df['userId'], train_df['movieId']],
                                    train_df['rating'],
                                    batch_size = 256,
                                    validation_split = 0.005,
                                    epochs = 4,
                                    verbose = 0)

pd.DataFrame(history_tabular1.history)

model_tabular.evaluate(x=[test_df['userId'],test_df['movieId']],y=test_df['rating'],verbose=0)

import numpy as np
pr = list(model_tabular.predict(x=[test_df['userId'],test_df['movieId']]))
predicted_ratings = list()
for i in range (0,len(pr)):
  predicted_ratings.append(pr[i][0])
#predicted_ratings = np.round_(predicted_ratings)
#print(predicted_ratings[:20])

userId = np.array(test_df['userId'])
movieId = np.array(test_df['movieId'])
actual_ratings = np.array(test_df['rating'])

# importing the required module
import matplotlib.pyplot as plt

plt.scatter(movieId[:500],actual_ratings[:500],label= "stars", color= "blue", marker= "*")
plt.scatter(movieId[:500],predicted_ratings[:500],label= "stars", color= "orange", marker= "*")
plt.title('Predicted vs Actual w.r.t MovieID')
plt.ylabel('ratings')
plt.xlabel('movieId')
plt.legend(['actual', 'predicted'], loc='upper left')
plt.show()

comparision2 = pd.DataFrame(list(zip(actual_ratings, predicted_ratings)), index = list(movieId),columns =['Actual', 'Predicted'])
comparision2