from jinja2 import Environment, FileSystemLoader

class Play:
    def __init__(self, name, note, players, receivers, blockers):
        self.name = name
        self.note = note
        self.players = players
        self.receivers = receivers
        self.blockers = blockers

class Player:
    def __init__(self, name, eligibility, blocking, xpos, ypos, direction, moves):
        self.name = name
        if eligibility:
            self.eligibility = 'circle'
        else:
            self.eligibility = 'rectangle'
        self.blocking = blocking
        self.xpos = xpos
        self.ypos = ypos
        self.direction = direction
        self.moves = moves

class Move:
    def __init__(self, xdir, ydir):
        self.xdir = xdir
        self.ydir = ydir

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('play.tex')

name = 'Name of the Play'
note = 'Special Notes'

players = [
        Player('wr1', True,  False, -25, -2.5, 'north',    [Move(0,4), Move( 3,0)]),
        Player('wr2', True,  False,  19, -1.5, 'north',    [Move(0,8), Move(-3,0)]),
        Player('wr3', True,  False,  22, -2.5, 'north',    [Move(0,8), Move(-3,3)]),
        Player('wr4', True,  False,  25, -2.5, 'north',    [Move(0,8), Move(-3,3)]),
        Player('te1', True,  True,   -9, -1.5, 'north',    [Move(0,1)]),
        Player('lt',  False, True,   -6, -1.5, 'north',    [Move(0,1)]),
        Player('lg',  False, True,   -3, -1.5, 'north',    [Move(0,1)]),
        Player('c',   False, True,    0, -1.5, 'north',    [Move(0,1)]),
        Player('rg',  False, True,    3, -1.5, 'north',    [Move(0,1)]),
        Player('rt',  False, True,    6, -1.5, 'north',    [Move(0,1)]),
        Player('qb',  True,  False,   0, -7.5, None,       [])
        ]

receivers = [p for p in players if p.moves and not p.blocking]
blockers = [p for p in players if p.blocking]

play = Play(name, note, players, receivers, blockers)

output_file = open('../build/play.tex', 'w')
output_file.write(template.render(play=play))
