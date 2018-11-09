from jinja2 import Environment, FileSystemLoader
from enum import Enum

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

def parse_players(players):
    players['wr1'] = Player('wr1', True,  -24, -2.5)
    players['wr2'] = Player('wr2', True,   18, -1.5)
    players['wr3'] = Player('wr3', True,   21, -2.5)
    players['wr4'] = Player('wr4', True,   24, -2.5)
    players['te1'] = Player('te1', True,   -9, -1.5)
    players['lt']  = Player('lt',  False,  -6, -1.5)
    players['lg']  = Player('lg',  False,  -3, -1.5)
    players['c']   = Player('c',   False,   0, -1.5)
    players['rg']  = Player('rg',  False,   3, -1.5)
    players['rt']  = Player('rt',  False,   6, -1.5)
    players['qb']  = Player('qb',  True,    0, -7.5)

def parse_routes(players):
    players['wr1'].set_base_route(Route(BaseRoute['CURL'], 13))
    players['wr2'].set_base_route(Route(BaseRoute['IN'], 7))
    players['wr3'].set_route('north',    [Move(0,8), Move(-3.5,3.5)])
    players['wr4'].set_base_route(Route(BaseRoute['POST'], 8))

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

    parse_players(players)
    parse_routes(players)
    parse_blocks(players)

    receivers = [p for p in players.values() if p.moves and not p.blocking]
    blockers = [p for p in players.values() if p.blocking]

    play = Play(name, note, players.values(), receivers, blockers)

    output_file = open('../build/play.tex', 'w')
    output_file.write(template.render(play=play))

if __name__ == '__main__':
    main()
