import pandas as pd 

outfile=open("MovieLens.sql",'w')

col_M = ['movie_id','non1','titleYear','non2','genres']
movies = pd.read_csv('movies.dat',sep = ':',names=col_M)

movies.drop('non1',axis = 1, inplace = True)
movies.drop('non2',axis = 1, inplace = True)

col_T = ['movie_id','non1', 'user_id','non2', 'tags','non3','Timestamp']
tags = pd.read_csv('tags.dat',sep = ':' , names= col_T)

tags.drop('non1',axis=1,inplace =True)
tags.drop('non2',axis=1,inplace =True)
tags.drop('non3',axis=1,inplace =True)


col_R = ['movie_id','non1', 'user_id','non2', 'ratings','non3','Timestamp']
ratings = pd.read_csv('ratings.dat', sep = ':', names = col_R)

ratings.drop('non1',axis=1,inplace = True)
ratings.drop('non2',axis=1,inplace =True)
ratings.drop('non3',axis=1,inplace =True)

L=len(movies[col_M[0]])


for i in range(L):
	outfile.write("insert into movies (movie_id, title, genres) values ('{}', '{}', '{}')\n".format(movies[col_M[0]][i],movies[col_M[2]][i],movies[col_M[4]][i]))

L=len(ratings[col_T[0]])
print("[X00]")

for i in range(L):
	outfile.write("insert into tags (user_id, movie_id, tag) values ('{}', '{}', '{}')\n".format(tags[col_T[2]][i],tags[col_T[0]][i],tags[col_T[4]][i]))

print("[XX0]")
L=len(ratings[col_R[0]])


for i in range(L):
	outfile.write("insert into ratings (user_id, movie_id, rating) values ('{}', '{}', '{}')\n".format(ratings[col_R[2]][i],ratings[col_R[0]][i],ratings[col_R[4]][i]))
print("[XXX]")
outfile.close()