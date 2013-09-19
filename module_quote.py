# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from datetime import date
import sqlite3
import re


COMMANDS = ['add', 'remove', 'find']

def init(botconfig):
    open_DB(True)


def open_DB(createTable=False):
    conn = sqlite3.connect('module_quote.db')
    c = conn.cursor()
    if createTable:
        c.execute('CREATE TABLE IF NOT EXISTS quotes (channel, date, user, quote);')
        conn.commit()
    return conn, c


def add_quote(channel, user, quote):
    conn, c = open_DB()
    today = date.today()
    c.execute('INSERT INTO quotes VALUES (?, ?, ?, ?);', (channel, today, user, quote))
    conn.commit()
    conn.close()
    return True

def random_quote(bot, user, channel):
    conn, c = open_DB()
    c.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1;')   
    quote = c.fetchone()[3]
    return bot.say(channel, quote)

def remove_quote(channel, quote):
    conn, c = open_DB()
    c.execute('DELETE FROM quotes WHERE quote = ?;', (quote, ))
    conn.commit()
    conn.close()
    return True
                             
def command_quote(bot, user, channel, args):
    """Usage: .quote [add|remove|find]"""

    if not args:
        return random_quote(bot, user, channel)

    args = args.split()
    command = args[0]
    if command not in COMMANDS:
        return bot.say(channel, 'Invalid command, valid commands are %s' % ', '.join(map(str, COMMANDS)))

    if command == 'add':
        if len(args) < 2:
            return bot.say(channel, 'Quote missing?')
        quote = " ".join(args[1:])
        
        add_quote(channel, user, quote)
        

    elif command == 'remove':
        if len(args) < 2:
            return bot.say(channel, 'Quote missing?')
        quote = " ".join(args[1:])
        remove_quote(channel, quote)
    elif command == 'find':
        if len(args) < 2:
            return bot.say(channel, 'Find needs some arguments')

        search = " ".join(args[1:])
        return find_quote(bot, user, channel, search)

def command_addquote(bot, user, channel, args):
    add_quote(channel, user, args.decode('utf-8'))

def find_quote(bot, user, channel, search):
    conn, c = open_DB()
    c.execute('SELECT * FROM quotes WHERE quote LIKE ?', ('%'+search+'%', ))
    row = c.fetchone()
    if row is not None:
        quote = row[3]
        return bot.say(channel, quote)    
