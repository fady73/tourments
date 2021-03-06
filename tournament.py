#!/usr/bin/env python
# tournament.py is an implementation of a Swiss-system tournament
# part of Project 4, FSND track with Udacity, Jan 18 2017

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        psycopg2.connect("dbname=tournament")
    except:
        print("Failed to connect")
    


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM match"
    c.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    query = "DELETE FROM players"
    c.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    query = "select count(*) from players"
    c.execute(query)
    data = c.fetchone()
    db.close()
    return data[0]


def registerPlayer(name):
    """
    Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    # return insert into players (name) values (%s) , %name
    db = connect()
    c = db.cursor()
	cmd = ('insert into players (name) values (%s)')
	c.execute(cmd, (name,))
	db.commit()
    db.close


def playerStandings():
    """
    Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = "select * from standings"
    c.execute(query)
    data = c.fetchall()
    db.close()
    return data


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    query = "insert into match (winner, loser) values (%s,%s)"
    c.execute(query, (winner, loser,))
    db.commit()
    db.close


def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
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
    db = connect()
    c = db.cursor()
    query = "with cte as(select *, ceiling(1.0 * row_number() over(order by wins) / 2) as rn from standings) select c1.Id, c1.Name, c2.Id, c2.name from cte c1 join cte c2 on c1.rn = c2.rn and c1.Id > c2.Id;" 

    c.execute(query)
    data = c.fetchall()
    db.close()
    return data