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
		ErNafnTil=False
		while ErNafnTil==False:
				Movie=str(input('\nSláðu inn nafnið á mynd sem þér líkar: ')).replace("'","''")
				x="""select * from movies where ((lower(title))) like lower('%{}%')""".format(Movie)
				cursor.execute(x)
				F=cursor.fetchall()
				if F!=[]:
					ErNafnTil=True
				else:
					print('Nafnið er vitlaust eða myndin er ekki til, reyndu aftur')
		try:
			MyndNR=0
			if len(F)>1:
				print('Fleiri en ein mynd er með þetta nafn, hverja af þessum myndum ert þú að tala um? ')
				for i in range(len(F)):
					print(i,F[i][1])
				print(i+1,'Velja aðra mynd')
				MyndNR=int(input())
			print(F[MyndNR][1])
			F=F[MyndNR][1].replace("'","''")
			x="""select movie_id from movies where title like '{}'""".format(F)
			cursor.execute(x)
			Reynduaftur=False
		except IndexError:
			print('Ósátt/-ur með valmöguleikana?')
		except ValueError:
			print('Þetta á að vera heiltala...\n')
	return cursor.fetchall()[0][0]

#movie fallið finnur nafn á myndinni og skilar movie_id, og endurtekur ef einhverjar eðlilegar villur gerast

Bool=True
while Bool:
	try:		
		x = int(input('Hversu margar myndir viltu lesa inn: '))
		Bool=False
	except ValueError:
		print('Þetta á að vera heiltala...\n')

Movie_id=[]
i=0
while i<x:
	M=movie()
	if M not in Movie_id:
		Movie_id.append(M)
		i+=1
	else:
		print('Þú ert búinn að velja þess mynd, reyndu aftur:')


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
""".format(Movie_id).replace('[','').replace(']','')
cursor.execute(x)

#SQL skipunin byrjar á að búa til view (svo við getum notað gögnin í öllum SQL skipunum)
#Í fyrri hluta skipunarinnar finnum við topp 50 notendurna sem hafa séð myndirnar sem við
#völdum og hafa gefið þeim einkunn yfir 3.5
#Í seinni hlutanum finnum við hversu margar myndir þessir notendur hafa gefið einkunn ásamt
#því að skipta listanum niður í Quartiles eftir þeim fjölda

L=[]
F=cursor.fetchall()
Bool1=False
Bool2=False
i=0
while Bool1==False:
	if Bool2==False and F[i][2]==2:
		Q2=F[i][1] #Fyrsta stak í Quarter 2 (Lowest)
		Bool2=True
	if F[i][2]==4:
		Q3=F[i-1][1] #Síðasta stak í Quarter 3 (Highest)
		Bool1=True
	i+=1
IQR=(Q3-Q2)*1.5
Q2-=IQR
Q3+=IQR	
Outlier=[]
for i in range(len(F)):
	if F[i][1]<Q2 or F[i][1]>Q3:
		Outlier.append(F[i][0])
print(Outlier)
#Reiknum Interquartile Range til að fjarlægja útlaga

x="""	
select title, avg(rating), count(title)
from likir_notendur natural join ratings natural join movies
where movie_id not in ({}) and user_id not in ({})
GROUP BY title
having avg(rating)>4
Order By count(title) DESC, avg(rating)
limit 10
""".format(Movie_id,Outlier).replace('[','').replace(']','')
cursor.execute(x)

#Finnum síðan myndir sem flestir hafa gefið einkunn og fær yfir  4 í rating eftir að það er búið að fjarlægja útlagana

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