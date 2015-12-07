create table movies (
	movie_id int ,
	title varchar(255),
	genres varchar(255) ,
	PRIMARY KEY(movie_id));

 create table ratings ( 
 	user_id int ,
 	movie_id int ,
 	rating int ,
 	timestamp int);

 create table tags (
 	user_id int ,
 	movie_id int ,
 	tag varchar(255),
 	timestamp int
 	);

LOAD DATA LOCAL INFILE 'movies.sql'
INTO TABLE movies
FIELDS TERMINATED BY '::'
LINES TERMINATED by '\n'

load DATA INFILE 'ratings.dat'
into table ratings
Fields Terminated by '::'
LINES Terminated by '\n'

load DATA INFILE 'tags.dat'
into table tags
Fields Terminated by '::'
LINES Terminated by '\n'


