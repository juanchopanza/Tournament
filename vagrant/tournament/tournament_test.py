#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    registerPlayer("Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "4. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney")
    registerPlayer("Joe Malik")
    registerPlayer("Mao Tsu-hsi")
    registerPlayer("Atlanta Hope")
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray")
    registerPlayer("Randy Schwartz")
    standings = playerStandings()
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 5:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, draws1, matches1),
     (id2, name2, wins2, draws2, matches2)] = standings
    if [wins1, draws1, matches1, wins2, draws2, matches2] != [0]*6:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)
    standings = playerStandings()
    for (i, n, w, d, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if d != 0:
            raise ValueError("Each player should have no draws recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testReportMatchesWithDraws():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    registerPlayer("Lucy Himmel")
    registerPlayer("Reto Schweitzer")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)
    reportMatch(id5, id6)  # No winner: this is a draw
    reportMatch(id3, id6)  # No winner: this is a draw
    reportMatch(id2, id3)  # No winner: this is a draw
    reportMatch(id2, id6, id2)
    standings = playerStandings()
    # standings are sorted by wins, then draws
    # matches have been reported such that playerStandings()
    # should guarantee this ordering (no players have equal number of
    # both wins and draws)
    ref_standings = [
        ('Cathy Burton', 1L, 2L, 3L),
        ("Boots O'Neal", 1L, 1L, 3L),
        ('Bruno Walton', 1L, 0L, 1L),
        ('Reto Schweitzer', 0L, 2L, 3L),
        ('Lucy Himmel', 0L, 1L, 1L),
        ('Diane Grant', 0L, 0L, 1L)
    ]

    for i, st in enumerate(standings):
        if st[1:] != ref_standings[i]:
            raise ValueError("Matches with draws not correctly ordered in standings")
    print "12. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


def testReportDuplicateMatchesRaisesValueError():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # this is already tested in testReportMatches()
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)

    def try_duplicate(a, b):
        ''' Attempt to report duplicate matches

        Returns:
            True if duplicate raises ValueError, False otherwise
        '''
        try:
            reportMatch(a, b, a)
        except ValueError:
            return True
        return False

    res = (try_duplicate(id1, id2)
           and try_duplicate(id3, id4)
           and try_duplicate(id2, id1)
           and try_duplicate(id4, id3))

    if not res:
        raise ValueError("Registering duplicate match did not raise ValueError")
    else:
        print "9. Registering duplicate matches raises"


def testReportSelfMatchesRaisesValueError():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # this is already tested in testReportMatches()
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)

    def try_self_match(a, b):
        ''' Attempt to report self matches

        Returns:
            True if a == b raises ValueError, False otherwise
        '''
        try:
            reportMatch(a, b, a)
        except ValueError:
            return True
        return False

    res = (try_self_match(id1, id1)
           and try_self_match(id2, id2)
           and try_self_match(id3, id3)
           and try_self_match(id4, id3))

    if not res:
        raise ValueError("Registering self-match did not raise ValueError")
    else:
        print "10. Registering match with self raises"

def testReportMatchesBadWinnerRaisesValueError():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton")
    registerPlayer("Boots O'Neal")
    registerPlayer("Cathy Burton")
    registerPlayer("Diane Grant")
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    # this is already tested in testReportMatches()
    reportMatch(id1, id2, id1)
    reportMatch(id3, id4, id3)

    def try_bad_winner_match(a, b, c):
        ''' Attempt to report match with invalid winner

        Returns:
            True if c not in (a, b) raises ValueError, False otherwise
        '''
        try:
            reportMatch(a, b, c)
        except ValueError:
            return True
        return False

    res = (try_bad_winner_match(id1, id2, id3)
           and try_bad_winner_match(id2, id3, id4)
           and try_bad_winner_match(id3, id4, id1)
           and try_bad_winner_match(id4, id1, id2))

    if not res:
        raise ValueError("Registering bad winner match did not raise ValueError")
    else:
        print "11. Registering match with bad winner raises"


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegister()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testReportDuplicateMatchesRaisesValueError()
    testReportSelfMatchesRaisesValueError()
    testReportMatchesBadWinnerRaisesValueError()
    testReportMatchesWithDraws()
    print "Success!  All tests pass!"
