from jinja2 import Environment, FileSystemLoader
from enum import Enum
import sys
import re

class Play:
    def __init__(self, name, note, players, receivers, blockers):
        self.name = name
        self.note = note
        self.players = players
        self.receivers = receivers
        self.blockers = blockers

class Player:
    def __init__(self, name, eligibility, xpos, ypos):
        self.name = name
        if eligibility:
            self.eligibility = 'circle'
        else:
            self.eligibility = 'rectangle'
        self.xpos = xpos
        self.ypos = ypos
        self.blocking = False
        self.direction = None
        self.moves = []

    def set_block(self, direction, moves):
        self.blocking = True
        self.direction = direction
        self.moves = moves

    def set_route(self, direction, moves):
        self.blocking = False
        self.direction = direction
        self.moves = moves

    def set_base_route(self, r):
        self.blocking = False
        self.direction = 'north'
        if self.xpos <= 0:
            direction = 1
        else:
            direction = -1
        switcher = {
                1: [Move(0, 1), Move(direction * -5, 0)],
                2: [Move(0, 1), Move(direction *  5, 2)],
                3: [Move(0, r.depth), Move(direction *  1.5, -1.5)],
                4: [Move(0, r.depth), Move(direction * -1.5, -1.5)],
                5: [Move(0, r.depth), Move(direction * -5,  0)],
                6: [Move(0, r.depth), Move(direction *  5,  0)],
                7: [Move(0, r.depth), Move(direction * -3.5,  3.5)],
                8: [Move(0, r.depth), Move(direction *  3.5,  3.5)],
                9: [Move(0, r.depth), Move(direction *  0, 17)],
                }
        self.moves = switcher[r.route.value]

class Move:
    def __init__(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir

class BaseRoute(Enum):
    FLAT = 1
    SLANT = 2
    COMEBACK = 3
    CURL = 4
    OUT = 5
    IN = 6
    CORNER = 7
    POST = 8
    GO = 9

class Route:
    def __init__(self, route, depth=0):
        self.depth = depth
        self.route = route

def parse_players(players, formation):
    formation_file = open('../build/formations/' + formation.replace(' ', '_'), 'r')
    for line in formation_file.readlines():
        line = line.strip()
        if line == '':
            continue
        match = re.match('(E|I)\s*([a-z]+[a-z0-9]*)\s*\(\s*([-+]?[0-9]*\.?[0-9]+)\s*,\s*([-+]?[0-9]*\.?[0-9]+)\s*\)', line, re.M|re.I)
        if match:
            groups = [match.group(1), match.group(2), match.group(3), match.group(4)]
            players[groups[1]] = Player(groups[1], groups[0] == 'E', float(groups[2]), float(groups[3]))
        else:
            print('Illegal syntax in file \'{}\': \'{}\''.format(formation, line))
            sys.exit(1)

def parse_routes(players, routes):
    routes = routes.strip()
    match = re.findall('(?:\s*([a-z]+[a-z0-9]*)\s+(FLAT|SLANT|GO|[0-9]+\s+(?:COMEBACK|CURL|OUT|IN|CORNER|POST))\s*)', routes, re.M|re.I)
    for (player, route) in match:
        rmatch = re.match('^([0-9]+)\s*(COMEBACK|CURL|OUT|IN|CORNER|POST)$', route, re.M|re.I)
        if rmatch:
            players[player].set_base_route(Route(BaseRoute[rmatch.group(2).upper()], rmatch.group(1)))
        else:
            rmatch = re.match('^(FLAT|SLANT|GO)$', route, re.M|re.I)
            if rmatch:
                players[player].set_base_route(Route(BaseRoute[rmatch.group(1).upper()]))
            else:
                print('Illegal route: \'{}\''.format(route))
    #players['wr1'].set_base_route(Route(BaseRoute['CURL'], 13))
    #players['wr2'].set_base_route(Route(BaseRoute['IN'], 7))
    #players['wr3'].set_route('north',    [Move(0,8), Move(-3.5,3.5)])
    #players['wr4'].set_base_route(Route(BaseRoute['POST'], 8))

def parse_blocks(players):
    players['te1'].set_block('north',    [Move(0,1)])
    players['lt'] .set_block('north',    [Move(0,1)])
    players['lg'] .set_block('north',    [Move(0,1)])
    players['c']  .set_block('north',    [Move(0,1)])
    players['rg'] .set_block('north',    [Move(0,1)])
    players['rt'] .set_block('north',    [Move(0,1)])

def main():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('play.tex')

    players = {}
    name = 'Name of the Play'
    note = 'Special Notes'

    parse_players(players, 'trips_right')
    parse_blocks(players)
    parse_routes(players, 'wr1 7 in wr2 slant wr3 8 post wr4 go')

    receivers = [p for p in players.values() if p.moves and not p.blocking]
    blockers = [p for p in players.values() if p.blocking]

    play = Play(name, note, players.values(), receivers, blockers)

    output_file = open('../build/play.tex', 'w')
    output_file.write(template.render(play=play))

if __name__ == '__main__':
    main()
