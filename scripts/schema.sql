----------- To enable foreign key on sqlite
PRAGMA foreign_keys = ON;

----------- Remove old tables
DROP TABLE IF EXISTS Casting;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS Movie;

----------- Movie table definition
CREATE TABLE Movie(
    movieid INTEGER PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    release VARCHAR(40),
    production VARCHAR(60),
    bio CHARACTER(10240),
    plot CHARACTER(10240)
);

----------- Actors table definition
CREATE TABLE Actor(
    actorid INTEGER PRIMARY KEY,
    fullname VARCHAR(30) NOT NULL,
    url VARCHAR(100),
    imageurl VARCHAR(100),
    born CHARACTER(1024)
);

----------- Actors table definition
CREATE TABLE Casting(
    castingid INTEGER PRIMARY KEY,
    actorid INTEGER NOT NULL,
    movieid INTEGER NOT NULL,
    FOREIGN KEY(movieid) REFERENCES Movie(movieid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(actorid) REFERENCES Actor(actorid) ON UPDATE CASCADE ON DELETE CASCADE
);
