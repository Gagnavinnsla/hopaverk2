create table movies (
	movie_id int ,
	title varchar(255),
	genres varchar(255) ,
	PRIMARY KEY(movie_id));

 create table ratings ( 
 	user_id int ,
 	movie_id int REFERENCES movies(movie_id),
 	rating float 
  	);

 create table tags (
 	user_id int ,
 	movie_id int REFERENCES movies(movie_id),
 	tag varchar(255)
  	);




