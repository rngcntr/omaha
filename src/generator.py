from jinja2 import Environment, FileSystemLoader

class Play:
    def __init__(self, name, note, players, receivers, blockers):
        self.name = name
        self.note = note
        self.players = players
        self.receivers = receivers
        self.blockers = blockers

class Player:
    def __init__(self, name, eligibility, xpos, ypos, direction, xdir, ydir, moves):
        self.name = name
        self.eligibility = eligibility
        self.xpos = xpos
        self.ypos = ypos
        self.direction = direction
        self.xdir = xdir
        self.ydir = ydir
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

wr1 = Player('wr1', 'circle', -25, -2.5, 'north', 0, 4, [Move(3,0)])
wr2 = Player('wr2', 'circle', 19, -1.5, 'north', 0, 8, [Move(-3,0)])
wr3 = Player('wr3', 'circle', 22, -2.5, 'north', 0, 8, [Move(-3,3)])
wr4 = Player('wr4', 'circle', 25, -2.5, 'north', 0, 8, [Move(-3,3)])

te1 = Player('te1', 'circle', -9, -1.5, 'north', 0, 1, [])
lt = Player('lt', 'rectangle', -6, -1.5, 'north', 0, 1, [])
lg = Player('lg', 'rectangle', -3, -1.5, 'north', 0, 1, [])
c = Player('c', 'rectangle', 0, -1.5, 'north', 0, 1, [])
rg = Player('rg', 'rectangle', 3, -1.5, 'north', 0, 1, [])
rt = Player('rt', 'rectangle', 6, -1.5, 'north', 0, 1, [])

qb = Player('qb', 'circle', 0, -7.5, None, None, None, [])

players = [wr1, wr2, wr3, wr4, te1, lt, lg, c, rg, rt, qb]
receivers = [p for p in players if p.moves]
blockers = [p for p in players if p.direction and not p.moves]

play = Play(name, note, players, receivers, blockers)

print(template.render(play=play))
