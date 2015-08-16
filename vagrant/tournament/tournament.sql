-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (id SERIAL PRIMARY KEY,
                      name VARCHAR(128) NOT NULL);


-- TODO: should this just winner_id, loser_id?
-- There is some reduncancy here. Initially I though it could be useful
-- to allow for draws, but this schema doesn't help that use-case either.
CREATE TABLE matches (id SERIAL PRIMARY KEY,
                      player_a_id INT REFERENCES players(id),
                      player_b_id INT REFERENCES players(id),
                      winner_id INT REFERENCES players(id));
