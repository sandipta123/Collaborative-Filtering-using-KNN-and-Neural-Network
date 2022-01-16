# Collaborative-Filtering-using-KNN-and-Neural-Network

## Collaborative Filtering using KNN
First, I imported all the necessary libraries. I have taken ratings and movies dataset from movielens 1m dataset.

Calculate the Nearest Neighbors.

Predict a Rating for a Movie by a User.

 The formula to calculate the predicted rating is as follows:
  R(m, u) = {∑ ⱼ S(m, j)R(j, u)}/ ∑ ⱼ S(m, j)
  •	R(m, u): the rating for movie m by user u
  •	S(m, j): the similarity between movie m and movie j
  •	j ∈ J where J is the set of the similar movies to movie m
  
 
## Neural Collaborative Filtering(NCF)
The aim is to build recommendation systems for explicit feedback systems where the task is to recommend items to users based on a rating matrix which is a matrix where cell (i,j) corresponds to the rating user ’i’ gave to item ’j’. Based on these ratings, the system tries to predict unfilled ratings in the matrix i.e. predicts intelligently what rating value an item might get by a user. 
