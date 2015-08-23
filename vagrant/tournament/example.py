#!/usr/bin/env python

from tournament import (registerPlayer,
                        registerPlayerToTournament,
                        registerTournament,
                        reportMatch,
                        playerStandings)

from pprint import pprint


if __name__ == '__main__':

    # Create some new tournaments
    t0 = registerTournament('t0')
    t1 = registerTournament('t1')

    # Register some players
    # Here, we register players to tournaments too
    # although that isn't strictly necessary.
    # It can be done in a separete step
    # using registerPlayerToTournament
    (id1, id2, id3, id4, id5, id6) = (
        registerPlayer("Bruno Walton", (t0, t1)),
        registerPlayer("Boots O'Neal", (t0, t1)),
        registerPlayer("Cathy Burton", (t0, t1)),
        registerPlayer("Diane Grant", (t0, t1)),
        registerPlayer("Lucy Himmel", (t0,)),
        registerPlayer("Reto Schweitzer")
    )

    # Register a player to a tournament
    registerPlayerToTournament(id6, t0)

    print 'Registered players', id1, id2, id3, id4, id5, id6
    print 'Standings tournament', t0, 'before playing any matches'
    pprint(playerStandings(t0))

    # report matches in tournament 0
    print 'Reporting matches in tournament', t0
    reportMatch(id1, id2, id1, t0)
    reportMatch(id3, id4, id3, t0)
    reportMatch(id5, id6, id5, t0)
    reportMatch(id1, id4, None, t0)  # This is a draw

    print 'Standings tournament', t0
    pprint(playerStandings(t0))

    # report matches in tournament 1
    print 'Reporting matches in tournament', t1
    reportMatch(id1, id2, id1, t1)
    reportMatch(id3, id4, None, t1)  # This is a draw

    standings = playerStandings(t0)

    print 'Standings tournament', t0
    pprint(standings)

    print 'Standings tournament', t1
    pprint(playerStandings(t1))
