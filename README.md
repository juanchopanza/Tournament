# Swiss Tournament

Project 2 in Udacity Fullstack Developer nanodegree

## Exciting extra features:

* No re-matches allowed.
* Games with no winner allowed: players with same number of wins are ranked by
  number of draws.


## Requirements:

This "application" is run and tested in a Lunix virtual machine managed by Vagrant.

These are the main requirements of the application. If using Vagrant, these will be
installed automatically. If running natively or on a manually installed virtual machine
you will need to ensure these dependencies are met.

* Python
* psycopg2
* PostgreSQL

## Installation

The installatioon is very simple:

0. Clone this repository
1. Initialize and boot the vagrant-managed VM
2. Log into it
3. Initialize the postgres database
4. Run the tests

### Clone this repository, initialize and boot the VM

    git clone https://github.com/juanchopanza/Tournament.git
    cd Tournament/vagrant/tournament
    vagrant up

### Log into the VM

    vagrant ssh
    cd /vagrant/tournament

### Initialize the database

The file `tournament.sql` contains the psql commands needed to initialize the tournament
database and populate it with the required tables. We can execute this file by passing
the appropriate command to `psql`:

    psql -c "\i tournament.sql"

### Run the tests

Simply run the `tournament_test.py` script:

    ./tournament_test.py

If this fails to run due to unsuitable permissions, invoke it with `python`:

    python tournament_test.py
