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

def movie():
	Reynduaftur=True
	while Reynduaftur==True:
		Bool=False
		while Bool==False:
				Movie=str(input('\nSláðu inn nafnið á mynd sem þér líkar: ')).replace("'","''")
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
			print(F.replace("''","'"))
			x="""select movie_id from movies where title like '{}'""".format(F)
			cursor.execute(x)
			Reynduaftur=False
		except IndexError:
			print('Ósátt/-ur með valmöguleikana?')
		except ValueError:
			print('Þetta á væntanlega að vera heiltala...\n')
	return cursor.fetchall()

Bool=True
while Bool:
	try:		
		x = int(input('Hversu margar myndir viltu lesa inn: '))
		Bool=False
	except ValueError:
		print('Þetta á væntanlega að vera heiltala...\n')
L=[]
N=[]
i=0
while i<x:
	M=movie()
	if M not in L:
		L.append(M)
		i+=1
	else:
		print('Þú ert búinn að velja þess mynd, reyndu aftur:')
	print(i)
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
select ln.user_id as Notandi_nr, count(movie_id) as Fjöldi_einkunna, ntile(4)
over (ORDER BY count(movie_id) ASC)
from likir_notendur ln join ratings r
    on r.user_id=ln.user_id
GROUP BY ln.user_id
""".format(N).replace('[','').replace(']','')
cursor.execute(x)
L=[]
F=cursor.fetchall()
Bool1=False
Bool2=False
i=0
while Bool1==False:
	if Bool2==False and F[i][2]==2:
		Q2=F[i][1]
		Bool2=True
	if F[i][2]==4:
		Q3=F[i-1][1]
		Bool1=True
	i+=1
IQR=(Q3-Q2)*1.5
Q2-=IQR
Q3+=IQR	
x="""	
select title, avg(rating), count(title)
from likir_notendur natural join ratings natural join movies
where movie_id not in ({})
GROUP BY title
having avg(rating)>4 and count(title) BETWEEN {} and {}
Order By count(title) DESC, avg(rating)
limit 10
""".format(N,Q2,Q3).replace('[','').replace(']','')
cursor.execute(x)
L=[]
F=cursor.fetchall()
for i in range(len(F)):
	L.append(F[i][0])
print('___________________________________________\n')
print('Við mælum með: \n')
[print(L[i],'\n') for i in range(len(L))]

conn.commit()
cursor.close()
conn.close()