-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS matches CASCADE;


CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name VARCHAR(128) NOT NULL);


CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      winner_id INT REFERENCES players(id),
                      loser_id INT REFERENCES players(id));
