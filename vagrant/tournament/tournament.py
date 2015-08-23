#!/usr/bin/env python
'''tournament.py -- implementation of a Swiss-system tournament'''

import psycopg2
from psycopg2 import IntegrityError
from itertools import izip_longest

DBNAME = 'tournament'


def connect(database_name=DBNAME):
    """Connect to the PostgreSQL database.

    Returns:
        Tuple of database connection, cursor.
    """
    db = psycopg2.connect("dbname=%s" % database_name)
    return db, db.cursor()


def _query(query, vals=(), commit=False, post_exec=None):
    '''Generic configurable query

    Returns:
        Result of the query

    TODO:
        Do we really neer to open and close each time?
    '''
    c, cur = connect()
    cur.execute(query, vals)
    if commit:
        c.commit()
    res = None if post_exec is None else post_exec(cur)
    c.close()
    return res


def _insert(query, vals=()):
    '''Insert a row and return its ID'''
    return _query(query, vals, commit=True, post_exec=lambda c: c.fetchone()[0])


def _select(query, vals=()):
    '''Select a row and return it'''
    return _query(query, vals, post_exec=lambda c: c.fetchall())


def _delete(query, vals=()):
    '''Delete a row'''
    _query(query, vals, commit=True)


def deleteTournaments():
    '''Remove all the tournaments from the database.'''
    _delete('DELETE FROM tournaments')


def deleteMatches(tournament=None):
    """Remove match records from the database.

    Args:
        tournament: id of tournament whose matches must be deleted. If
                    None, all matches are deleted.
    """
    if tournament is not None:
        _delete('DELETE FROM matches WHERE tournament_id = %s',
                (tournament,))
    else:
        _delete('DELETE FROM matches')


def deletePlayers():
    """Remove all the player records from the database."""
    _delete('DELETE FROM players')


def countPlayers():
    """Returns the number of players currently registered."""
    return _select('SELECT COUNT(*) from players;')[0][0]


def registerTournament(name):
    """Adds a tournament to the tournament database.

    Args:
      name: the tournament's name (need not be unique).

    Returns:
        id of the registered tournament
    """
    return _insert('INSERT INTO tournaments(name) VALUES (%s) RETURNING id', (name,))


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    return _insert('INSERT INTO players(name) VALUES (%s) RETURNING id', (name,))


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tournament: id of the torunament whose standings are to be calculated

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # This is  not a view because I need to parametrize by tournament ID at
    # runtime.
    standings_query = '''
    SELECT players.id as id,
       players.name as name,
       (SELECT COUNT(*) FROM matches WHERE players.id = matches.winner_id) as wins,
       (SELECT COUNT(*) FROM matches WHERE (players.id = matches.player_a_id or
                                            players.id = matches.player_b_id) and
                                            matches.winner_id IS NULL) as draws,
       (SELECT COUNT(*) FROM matches WHERE players.id = matches.player_a_id or
                                           players.id = matches.player_b_id) as matches
    FROM players, tournaments where tournaments.id = %s
    ORDER BY wins DESC, draws DESC;
    '''
    return _select(standings_query, (tournament,))


def reportMatch(player_a, player_b, winner=None, tournament=None):
    """Records the outcome of a single match between two players.

    Args:
      player_a:  the id number of the first player
      player_b:  the id number of the second player
      winner: the id of the winner. None in case of draw.
      tournament: id of the torunament match is being played in.

    Raises:
        IntegrityError if pairing already registered or player_a == player_b.
        IntegrityError if winner is not player_a or player_b or None.
        IntegrityError if players already played.
    """

    def _checkPairing():
        q = '''
        SELECT COUNT(*) FROM matches, tournaments
        WHERE tournaments.id = %s
              AND (matches.player_a_id = %s AND matches.player_b_id = %s)
              OR (matches.player_a_id = %s AND matches.player_b_id = %s);
        '''
        res = _select(q, (tournament, player_a, player_b, player_b, player_a))
        if res[0][0] > 0:
            raise ValueError('Pairing %s, %s already played' % (player_a, player_b))

    _checkPairing()

    return _insert('INSERT INTO matches(tournament_id, player_a_id, player_b_id, winner_id) VALUES (%s, %s, %s, %s) RETURNING id',
                   (tournament, player_a, player_b, winner))


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
        tournament: id of the tournament pairings are requested for.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

    Raises:
        ValueError if the number of players registered in tournamennt is odd.
    """

    # Standings lists players ordered by number of wins. We construct the
    # swiss pairings from consecutive entries in the standings list. These have
    # the closest number of wins by definition.
    # We use a grouper function to iterate over the standings list in groups
    # of two consecutive elements without overlap.

    def grouper(iterable, n, fillvalue=None):
        '''Collect data into fixed-length chunks or blocks

        Taken from  itertools documentation:
            https://docs.python.org/2/library/itertools.html

        grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        '''
        args = [iter(iterable)] * n
        return izip_longest(fillvalue=fillvalue, *args)

    standings = playerStandings(tournament)

    if len(standings) % 2 != 0:
        raise ValueError('Odd number of players not supported')

    pairings = [(a[0], a[1], b[0], b[1])
                for a, b in grouper(standings, 2)]

    return pairings
