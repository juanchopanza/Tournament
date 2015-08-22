-- Table definitions for the tournament project.
--
-- WARNING: This script re-creates the database from scratch each time.
--          Previously stored data will be lost!

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;


CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name VARCHAR(128) NOT NULL);


-- redundant IDs needed to support draws.
-- winner_id is NULL if the match is a draw.
CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      player_a_id INT REFERENCES players(id) NOT NULL,
                      player_b_id INT REFERENCES players(id) NOT NULL,
                      winner_id INT REFERENCES players(id));


CREATE VIEW standings as
SELECT players.id as id,
       players.name as name,
       (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner_id) as wins,
       (SELECT COUNT(*) FROM matches WHERE (players.id = matches.player_a_id or
                                            players.id = matches.player_b_id) and
                                            matches.winner_id IS NULL) as draws,
       (SELECT COUNT(*) FROM matches WHERE players.id = matches.player_a_id or
                                           players.id = matches.player_b_id) as matches
FROM players ORDER BY wins DESC, draws DESC;
