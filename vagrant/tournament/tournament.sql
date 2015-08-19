-- Table definitions for the tournament project.
--
-- WARNING: This script re-creates the database from scratch each time.
--          Previously stored data will be lost!

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;


CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name VARCHAR(128) NOT NULL);


CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      winner_id INT REFERENCES players(id),
                      loser_id INT REFERENCES players(id));


CREATE VIEW standings as
SELECT players.id as id,
       players.name as name,
       (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner_id) as wins,
       (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner_id or
                                           players.id = matches.loser_id) as matches
FROM players ORDER BY wins DESC;
