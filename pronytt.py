import pandas as pd 
import psycopg2
import getpass


host = 'localhost'
dbname = 'movies'

username = 'postgres'
pw = 'postgres'
conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")

col_M = ['movie_id','non1','titleYear','non2','genres']
movies = pd.read_csv('movies.dat',sep = ':',names=col_M)

movies.drop('non1',axis = 1, inplace = True)
movies.drop('non2',axis = 1, inplace = True)

col_T = ['user_id','non1','movie_id','non2','ratings','non3','Timestamp']
tags = pd.read_csv('tags.dat',sep = ':' , names= col_T)

tags.drop('non1',axis=1,inplace =True)
tags.drop('non2',axis=1,inplace =True)
tags.drop('non3',axis=1,inplace =True)


col_R = ['user_id','non1','movie_id','non2','ratings','non3','Timestamp']
ratings = pd.read_csv('ratings.dat', sep = ':', names = col_R)

ratings.drop('non1',axis=1,inplace = True)
ratings.drop('non2',axis=1,inplace =True)
ratings.drop('non3',axis=1,inplace =True)

L=len(movies[col_M[0]])
print(L)


for i in range(L):
	command="""insert into movies (movie_id, title, genres) values ('{}', '{}', '{}')\n""".format(movies[col_M[0]][i],movies[col_M[2]][i].replace(",","/").replace("'","''"),movies[col_M[4]][i])
	print(command)
	cursor.execute(command)

L=len(tags[col_T[0]])
print(L)

for i in range(L):
	command="""insert into tags (movie_id, user_id, tag) values ("{}", "{}", "{}")\n""".format(tags[col_T[2]][i],tags[col_T[0]][i],tags[col_T[4]][i])
	cursor.execute(command)
		
print("[XX0]")
L=len(ratings[col_R[0]])


for i in range(L):
	command="""insert into ratings (movie_id, user_id, rating) values ("{}", "{}", "{}")\n""".format(ratings[col_R[2]][i],ratings[col_R[0]][i],ratings[col_R[4]][i])
	cursor.execute(command)
print("[XXX]")

conn.commit()

cursor.close()
conn.close()