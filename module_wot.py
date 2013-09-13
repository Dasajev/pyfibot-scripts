"""
Get World of Tanks statistics from Planet WOT
"""

from __future__ import unicode_literals, print_function, division
from bs4 import BeautifulSoup
import datetime
import time

server = 'eu'
baseurl = 'http://www.planetwot.com/playerStats/?name=%s&d=%s'


def command_wot(bot, user, channel, args):
    """Get the player info"""
    result = getinfo(bot, args)

    return bot.say(channel, result.encode("UTF-8"))


def getinfo(bot, player):
    """Parse the package status page"""
    url = baseurl % (player, server)
    r = bot.get_url(url)
    bs = BeautifulSoup(r.content)
    if not bs:
        return

    res = []

    table = bs.find("table", {'class': "statistics"})
    rows = list()
    for row in table.findAll("tr"):
        rows.append(row)

    for row in rows:
        cells = row.findChildren('td');
        if len(cells) >= 2:
            if cells[0].string is not None and cells[1].string is not None:
                res.append(cells[0].string)
                res.append(" ")
                res.append(cells[1].string)
                res.append(" ")

    str = "".join(res)
    return str
