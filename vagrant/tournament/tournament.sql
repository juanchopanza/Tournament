-- Table definitions for the tournament project.
--
-- WARNING: This script re-creates the database from scratch each time.
--          Previously stored data will be lost!

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;


CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name VARCHAR(128) NOT NULL);


CREATE TABLE tournaments (id SERIAL PRIMARY KEY,
                          name VARCHAR(128) NOT NULL);


-- redundant IDs needed to support draws.
-- winner_id is NULL if the match is a draw.
CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      tournament_id INT REFERENCES tournaments(id) ON DELETE CASCADE NOT NULL,
                      player_a_id INT REFERENCES players(id) ON DELETE CASCADE NOT NULL,
                      player_b_id INT REFERENCES players(id) ON DELETE CASCADE NOT NULL,
                      winner_id INT REFERENCES players(id));
