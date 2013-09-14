"""
Get World of Tanks statistics from NoobMeter
"""

from __future__ import unicode_literals, print_function, division
from bs4 import BeautifulSoup
import re

server = 'eu'
baseurl = 'http://www.noobmeter.com/player/%s/%s'


def command_wot(bot, user, channel, args):
    result = getinfo(bot, args)

    return bot.say(channel, result.encode("UTF-8"))

def get_data_for_row(row):
    cells = row.findChildren('td');
    if len(cells) >= 2:
        if cells[1].string is None:
            for string in cells[1].strings:
                return string
        else:
            return cells[1].string

    return None

def getinfo(bot, player):
    url = baseurl % (server, player)
    r = bot.get_url(url)
    bs = BeautifulSoup(r.content)
    if not bs:
        return

    res = []

    table = bs.find("table", {'class': "tablesorter"})
    if not table:
        return "Player not found"
    rows = list()
    for row in table.findAll("tr"):
        rows.append(row)

    res.append(player)
    res.append(", Games: ")
    games = get_data_for_row(rows[6])
    res.append(games.strip())

    res.append(" - ")

    winp_string = get_data_for_row(rows[7])
    non_decimal = re.compile(r'[^\d.]+')
    winp = float(non_decimal.sub('', winp_string))/100.0    
    games_number = int(non_decimal.sub('', games))
    wins = int(games_number*winp)
    win_string = "Wins: %d (%s)" % (wins, winp_string.strip())
    res.append(win_string)

    res.append(" - ")

    res.append("K:D: ")
    kd = get_data_for_row(rows[15])
    res.append(kd.strip())

    #Missing: Destroyed, Hit%

    res.append(" - ")

    res.append("AvgXp: ")
    avgexp = get_data_for_row(rows[9])
    res.append(avgexp.strip())

    res.append(", Eff: ")
    eff = get_data_for_row(rows[2])
    res.append(non_decimal.sub("", eff.strip()))

    res.append(", WN7: ")
    wn7 = get_data_for_row(rows[4])
    res.append(non_decimal.sub("", wn7.strip()))
    
    str = "".join(res)
    return str
