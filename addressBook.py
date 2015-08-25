## Write a small app that takes in name, phone number, and email address from the command line input and stores it in an SQLlite local database. 
## This tool must include a function to display the entire contents of the database in a clear, human-readable format on the screen, with each entry numbered.
## Completed by: David Gunter

## Instructions:
## from the command line, run: `python addressBook.py add NAME PHONENUMBER EMAIL` to add a new user
## Run `python addressBook.py show` to list all users in the database.

import sqlite3, argparse

def _connectDB():
    """ 
        Provides a simple way to connect to our DB.
        Returns a connection object
    """
    conn = sqlite3.connect('addressBook.db')

    #Set the row_factory to let us call row values by column name
    conn.row_factory = sqlite3.Row
    return conn


def addUser(args):
    """ 
        Inserts user into database with passed CLI arguments
    """
    db = _connectDB()

    db.execute('INSERT INTO users (name, phone, email) VALUES (?, ?, ?)', (args.name, args.phone, args.email))
    db.commit()
    db.close()
    print "--- User added successfully ---"

def showAllUsers(args):
    """
        Prints out a list of all users in the database,
        Formats the returned rows for easier reading
    """

    db = _connectDB()

    # Print headers for the output
    print "%-5s %-30s %-13s %-30s \r" % ('ID ', 'Name', 'Phone', 'Email')
    
    for row in db.execute('SELECT * FROM users ORDER BY id'):
        # Pretty print the rows
        print "%-5s %-30s %-13s %-30s \r" % (row['id'], row['name'], row['phone'], row['email'])

    db.close()



def main():

    # Init CLI argument parsers
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Subcommand help')

    ## Add new user to our db
    parser_addUser = subparsers.add_parser('add', help='Add user to the database')
    parser_addUser.set_defaults(func=addUser) 
    parser_addUser.add_argument('name', help='Name of the user')
    parser_addUser.add_argument('phone', type=int, help='Phone number of user. Format WITHOUT dashes (-) or parentheses.')
    parser_addUser.add_argument('email', help='Email of the user')

    ## Print all users
    parser_showAll = subparsers.add_parser('show', help='List all users from the database')
    parser_showAll.set_defaults(func=showAllUsers)


    ## Final setup for parsing CLI arguments
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
