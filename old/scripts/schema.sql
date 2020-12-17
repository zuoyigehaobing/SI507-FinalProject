----------- To enable foreign key on sqlite
PRAGMA foreign_keys = ON;

----------- Remove old tables
DROP TABLE IF EXISTS Casting;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS Users;

----------- Movie table definition
CREATE TABLE Movie(
    movieid INTEGER PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    release VARCHAR(40),
    production VARCHAR(60),
    url VARCHAR(100),
    img VARCHAR(100),
    bio CHARACTER(8000),
    plot CHARACTER(8000)
);

----------- Actors table definition
CREATE TABLE Actor(
    actorid INTEGER PRIMARY KEY,
    fullname VARCHAR(30) NOT NULL,
    url VARCHAR(100),
    imageurl VARCHAR(100)
);

----------- Actors table definition
CREATE TABLE Casting(
    actorid INTEGER NOT NULL,
    movieid INTEGER NOT NULL,
    PRIMARY KEY(actorid, movieid),
    FOREIGN KEY(movieid) REFERENCES Movie(movieid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(actorid) REFERENCES Actor(actorid) ON UPDATE CASCADE ON DELETE CASCADE
);

----------- User table definition
CREATE TABLE Users(
	username VARCHAR(20) NOT NULL,
	fullname VARCHAR(40) NOT NULL,
	email VARCHAR(40) NOT NULL,
	password CHARACTER(256) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(username)
);


CREATE TABLE Likes(
	owner VARCHAR(20) NOT NULL,
	movieid int NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(owner, movieid),
	FOREIGN KEY(owner) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(movieid) REFERENCES Movie(movieid) ON UPDATE CASCADE ON DELETE CASCADE
);


-- user1 follows user2
CREATE TABLE Following(
	user1 VARCHAR(20) NOT NULL,
	user2 VARCHAR(20) NOT NULL,
	created DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(user1, user2),
	FOREIGN KEY(user1) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(user2) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE
);