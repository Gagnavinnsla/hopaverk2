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

def movie():

	Bool=False
	Reynduaftur=True
	while Reynduaftur==True:
		while Bool==False:
				Movie=str(input('\nSláðu inn nafnið á mynd sem þér líkar: '))
				x="""select * from movies where ((lower(title))) like lower('%{}%')""".format(Movie)
				cursor.execute(x)
				F=cursor.fetchall()
				if F!=[]:
					Bool=True
				else:
					print('Nafnið er vitlaust eða myndin er ekki til, reyndu aftur')
		try:
			Tmp=0
			if len(F)>1:
				print('Fleiri en ein mynd er með þetta nafn, hverja af þessum myndum ert þú að tala um ')
				for i in range(len(F)):
					print(i,F[i][1])
				print(i+1,'Velja aðra mynd')
				Tmp=int(input())
			F=F[Tmp][1].replace("'","''")
			print(F)
			x="""select movie_id from movies where title like '{}'""".format(F)
			cursor.execute(x)
			Reynduaftur=False
		except IndexError:
			print('Ósátt/-ur með valmöguleikana?')
			return
	return cursor.fetchall()

		
x = int(input('Hversu margar myndir viltu lesa inn: '))
L=[]
N=[]
for i in range(x):
	L.append(movie())
for i in range(len(L)):
	N.append(L[i][0][0])

x="""
CREATE OR REPLACE VIEW likir_notendur AS
select user_id, count(user_id), avg(rating)
from movies natural join ratings
where rating > 3.5 and movie_id in ({})
GROUP BY user_id
ORDER BY count(user_id) desc, avg(rating) desc
limit 50
;

select title, avg(rating), count(title)
from likir_notendur natural join ratings natural join movies
where movie_id not in ({})
GROUP BY title
HAVING avg(rating)>4
Order By count(title) DESC, avg(rating) DESC
limit 10
""".format(N,N).replace('[','').replace(']','')
cursor.execute(x)
L=[]
F=cursor.fetchall()
for i in range(len(F)):
	L.append(F[i][0])
print('___________________________________________\n')
print('Við mælum með: \n')
[print(i,L[i],'\n') for i in range(len(L))]


conn.commit()
cursor.close()
conn.close()