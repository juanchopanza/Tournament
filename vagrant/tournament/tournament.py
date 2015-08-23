#!/usr/bin/env python
'''tournament.py -- implementation of a Swiss-system tournament

Allows multpile tournaments and draws.

Author: Juan Palacios

'''

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


def deleteTournamentPlayers(tournament=None):
    """Remove tournamend player registries from the database.

    Args:
        tournament: id of tournament whose matches player registry will be deleted.
                    If None, all registries are deleted.
    """
    if tournament is not None:
        _delete('DELETE FROM tournament_players WHERE tournament_id = %s',
                (tournament,))
    else:
        _delete('DELETE FROM tournament_players')


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


def registerPlayer(name, tournaments=()):
    """Adds a player to the global tournament database.

    Args:
      name: the player's full name (need not be unique).
      tournament(optional): Iterable with IDs if tournaments to which this player
      should be registered.

      Note:
          Players can be registered to tournaments separately
          using the registerPlayerToTournament method.

    Returns:
        ID of registered player
    """
    player_id = _insert('INSERT INTO players(name) VALUES (%s) RETURNING id', (name,))
    for tournament_id in tournaments:
        registerPlayerToTournament(player_id, tournament_id)

    return player_id


def tournamentPlayers(tournament):
    '''Return tuple of player IDs of players registered in tournament'''
    res = _select('SELECT player_id FROM tournament_players WHERE tournament_id = %s',
                  (tournament,))
    return tuple(p[0] for p in res)


def registerPlayerToTournament(player_id, tournament_id):
    '''Register an existing player to a tournament

    Note:
        Registering a player more than once in the same tournament is an error.

    Raises:
        IntegrityError if registration failed.
    '''
    return _query('INSERT INTO tournament_players(player_id, tournament_id) VALUES (%s, %s)',
                  (player_id, tournament_id),
                  commit=True)


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tournament: id of the torunament whose standings are to be calculated

    Returns:
      A list of tuples, each of which contains
      (id, name, wins, draws, matches, points):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: Number of games won in this tournament
        draws: Number of games drawn in this tournament
        matches: the number of matches played by the player in this tournament
        points: the number of points scored by the player has scored in this tournament
    """

    standings_query = '''
    SELECT id, name, wins, draws, matches, points FROM standings WHERE tournament_id = %s
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
        ValueError if players already played each other in this tournament.
        ValueError if either player isn't registered in the tournament.
        IntegrityError if player_a == player_b.
        IntegrityError if winner is not player_a or player_b or None.
    """

    def _checkPlayersRegistered():
        '''Check that both players are registered in the tournament'''
        players = tournamentPlayers(tournament)
        if player_a not in players or player_b not in players:
            raise ValueError(
                "At least one of players %s, %s isn't registered in tournament %s"
                % (player_a, player_b, tournament))

    def _checkNewMatch():
        '''Check that this match hasn't already been reported'''
        q = '''
        SELECT COUNT(*) FROM matches, tournaments
        WHERE matches.tournament_id = tournaments.id AND tournaments.id = %s
              AND (matches.player_a_id = %s AND matches.player_b_id = %s)
              OR (matches.player_a_id = %s AND matches.player_b_id = %s);
        '''
        res = _select(q, (tournament, player_a, player_b, player_b, player_a))
        if res[0][0] > 0:
            raise ValueError('Pairing %s, %s already played in tournament %s'
                             % (player_a, player_b, tournament))

    _checkPlayersRegistered()
    _checkNewMatch()

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

    # Standings lists players ordered by points, where 2 and 1 points
    # are awarded for a win and draw respectively. We construct the
    # swiss pairings from consecutive entries in the standings list. These have
    # the closest number of points by definition.
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
