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


-- Table of all match results
-- Result score: 2, 1, 0 points for win, draw, loss respectively
-- For CASE see http://www.postgresql.org/docs/9.3/static/plpgsql-control-structures.html
CREATE VIEW results_table AS
SELECT players.id AS player_id,
       players.name AS player_name,
       tournament_players.tournament_id,
       matches.id AS match_id,
CASE
    WHEN matches.id IS NOT NULL AND players.id = matches.winner_id
        THEN 2
    WHEN matches.id IS NOT NULL AND matches.winner_id is NULL
        THEN 1
    ELSE 0
END AS result
FROM players INNER JOIN tournament_players ON players.id = tournament_players.player_id
     LEFT JOIN matches ON matches.tournament_id = tournament_players.tournament_id AND
                          (players.id = matches.player_a_id OR players.id = matches.player_b_id);


-- Player standings, ordered by tournament id and points scored
-- Player standings are grouped by tournament id such that statistics
-- can ge gathered for individual tournaments
CREATE VIEW standings AS
SELECT player_id AS id,
       player_name AS name,
       SUM(CASE WHEN match_id IS NOT NULL THEN 1 ELSE 0 END) AS matches,
       SUM(CASE WHEN match_id IS NOT NULL AND result = 2 THEN 1 ELSE 0 END) AS wins,
       SUM(CASE WHEN match_id IS NOT NULL AND result = 1 THEN 1 ELSE 0 END) AS draws,
       SUM(CASE WHEN match_id IS NOT NULL AND result = 0 THEN 1 ELSE 0 END) AS losses,
       SUM(result) AS points,
       tournament_id
FROM results_table
GROUP BY player_name, player_id, tournament_id
ORDER BY tournament_id, points DESC, wins DESC;
