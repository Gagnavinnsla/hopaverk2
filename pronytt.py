import pandas as pd 

col_M = ['movie_id','non1','titleYear','non2','genres']
movies = pd.read_csv('movies.dat',sep = ':',names=col_M)

movies.drop('non1',axis = 1, inplace = True)
movies.drop('non2',axis = 1, inplace = True)

col_T = ['movie_id','non1', 'user_id','non2', 'tags','non3','Timestamp']
tags = pd.read_csv('tags.dat',sep = ':' , names= col_T)

tags.drop('non1',axis=1,inplace = True)
tags.drop('non2',axis=1,inplace =True)
tags.drop('non3',axis=1,inplace =True)


col_R = ['movie_id','non1', 'user_id','non2', 'ratings','non3','Timestamp']
ratings = pd.read_csv('ratings.dat', sep = ':', names = col_R)

ratings.drop('non1',axis=1,inplace = True)
ratings.drop('non2',axis=1,inplace =True)
ratings.drop('non3',axis=1,inplace =True)


