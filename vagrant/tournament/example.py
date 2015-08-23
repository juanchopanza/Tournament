#!/usr/bin/env python

from tournament import *


def printStandings(standings):
    for s in standings:
        print s


if __name__ == '__main__':

    deletePlayers()
    deleteMatches()
    deleteTournaments()
    deleteTournamentPlayers()

    # Register some tournaments
    t0 = registerTournament('t0')
    t1 = registerTournament('t1')


    # Register some players
    (id1, id2, id3, id4, id5, id6) = (
        registerPlayer("Bruno Walton", (t0, t1)),
        registerPlayer("Boots O'Neal", (t0, t1)),
        registerPlayer("Cathy Burton", (t0, t1)),
        registerPlayer("Diane Grant", (t0, t1)),
        registerPlayer("Lucy Himmel", (t0,)),
        registerPlayer("Reto Schweitzer", (t0,))
    )

    print 'Registered players', id1, id2, id3, id4, id5, id6
    print 'Standings tournament', t0, 'before playing any matches'
    printStandings(playerStandings(t0))

    # report matches in tournament 0
    print 'Reporting matches in tournament', t0
    reportMatch(id1, id2, id1, t0)
    reportMatch(id3, id4, id3, t0)
    reportMatch(id5, id6, id5, t0)
    reportMatch(id1, id4, None, t0)

    print 'Standings tournament', t0
    printStandings(playerStandings(t0))

    # report matches in tournament 1
    print 'Reporting matches in tournament', t1
    reportMatch(id1, id2, id1, t1)
    reportMatch(id3, id4, None, t1)

    standings = playerStandings(t0)

    print 'Standings tournament', t0
    printStandings(standings)

    print 'Standings tournament', t1
    printStandings(playerStandings(t1))


