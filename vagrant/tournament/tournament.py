#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

DBNAME = 'tournament'

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=%s" % DBNAME)


def _commit(query):
    '''Connext, commit query, and close

    TODO:
        Do we really neer to open and close each time?
    '''
    c = connect()
    c.cursor().execute(query)
    c.commit()
    c.close()


def deleteMatches():
    """Remove all the match records from the database."""
    _commit('DELETE FROM matches')

def deletePlayers():
    """Remove all the player records from the database."""
    _commit('DELETE FROM players')


def countPlayers():
    """Returns the number of players currently registered."""
    c = connect()
    cur = c.cursor()
    cur.execute('SELECT COUNT(*) from players;')
    res = cur.fetchone()[0]
    c.close()
    return res


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    c = connect()
    c.cursor().execute('INSERT INTO players(name) VALUES (%s)', (name,))
    c.commit()
    c.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    pass


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    pass


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pass
