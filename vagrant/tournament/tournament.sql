-- Table definitions for the tournament project.
--
-- WARNING: This script re-creates the database from scratch each time.
--          Previously stored data will be lost!

-- Disconnect all existing database connections before dropping.
-- See http://stackoverflow.com/questions/5408156/how-to-drop-a-postgresql-database-if-there-are-active-connections-to-it
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament';

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;


CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);


CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

-- Store players registered in a certain tournament
CREATE TABLE tournament_players (
    tournament_id INT REFERENCES tournaments(id) ON DELETE CASCADE NOT NULL,
    player_id INT REFERENCES players(id) ON DELETE CASCADE NOT NULL,
    PRIMARY KEY (tournament_id, player_id)
); 

-- redundant IDs needed to support draws.
-- winner_id is NULL if the match is a draw.
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    tournament_id INT REFERENCES tournaments(id) ON DELETE CASCADE NOT NULL,
    player_a_id INT REFERENCES players(id) ON DELETE CASCADE NOT NULL,
    player_b_id INT REFERENCES players(id) ON DELETE CASCADE NOT NULL,
    winner_id INT REFERENCES players(id),
    CHECK (player_a_id <> player_b_id),
    CHECK (player_a_id = winner_id OR
        player_b_id = winner_id OR
        winner_id is NULL)
);
