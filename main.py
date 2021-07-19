import pygame
import random
import ctypes

import game
import mortgage
from functions import *

ctypes.windll.user32.SetProcessDPIAware()

class Var:
    pass

var = Var()

init(var)

var.screen = pygame.display.set_mode((1624, 1024))
pygame.display.set_caption('大富翁')

pygame.init()

var.fpsclock = pygame.time.Clock()

var.board = pygame.image.load('images/board.jpg')
var.house = pygame.image.load('images/house.png')
var.hotel = pygame.image.load('images/hotel.png')
var.moneys = {}
for i in [1, 5, 10, 20, 50, 100, 500]:
    var.moneys[i] = pygame.image.load('images/moneys/money%s.jpg' % i)
var.dices = []
for i in range(1, 7):
    var.dices.append(pygame.transform.smoothscale(pygame.image.load('images/dices/dice%s.png' % i), (100, 100)))
var.dice_s = []
for i in range(1, 7):
    var.dice_s.append(pygame.transform.smoothscale(pygame.image.load('images/dices/dice_%s.png' % i), (100, 100)))

var.font_fangsong30 = pygame.font.SysFont('fangsong', 30)
var.font_fangsong35 = pygame.font.SysFont('fangsong', 35)
var.font_fangsong40 = pygame.font.SysFont('fangsong', 40)
var.font_aerial26 = pygame.font.SysFont('aerial', 26)
var.font_simhei22 = pygame.font.SysFont('simhei', 22)
var.font_simhei30 = pygame.font.SysFont('simhei', 30)

class Card:
    def __init__(self, name, price, rent, _type, index):
        self.name = name
        self.price = price
        self.index = index
        self.turns = -1
        self.house = 0
        self.owner = None
        self.rent = rent
        self.type = _type
        hx = hy = None
        ii = index // 10
        if index % 10 != 0:
            num = index % 10
            if ii % 2 == 0:
                w = 84
                h = 134
            else:
                w = 134
                h = 84
            if ii == 0:
                x = (num - 1) * 84 + 134
                y = 0
                hx = x
                hy = 102
            elif ii == 1:
                x = 890
                y = (num - 1) * 84 + 134
                hx = x
                hy = y
            elif ii == 2:
                x = 890 - num * 84
                y = 890
                hx = x
                hy = y
            elif ii == 3:
                x = 0
                y = 890 - num * 84
                hx = 102
                hy = y
        else:
            if ii in (0, 3):
                x = 0
            else:
                x = 890
            if ii in (0, 1):
                y = 0
            else:
                y = 890
            w = h = 134
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hx = hx
        self.hy = hy
        self.rect = pygame.Rect(x, y, w, h)
    def draw(self):
        color = (0, 255, 0) if self.owner == var.player else (255, 0, 0)
        pygame.draw.rect(var.screen, color, self.rect, 2)
        if self.house < 5:
            if self.w == 84:
                if self.house % 2 == 0:
                    for i in range(self.house):
                        var.screen.blit(var.house, ((3 - self.house) * 15 + self.hx + i * 30, self.hy))
                else:
                    for i in range(self.house):
                        var.screen.blit(var.house, ((3 - self.house) * 15 + self.hx + i * 30, self.hy))
            elif self.w == 134:
                if self.house % 2 == 0:
                    for i in range(self.house):
                        var.screen.blit(var.house, (self.hx, (3 - self.house) * 15 + self.hy + i * 30))
                else:
                    for i in range(self.house):
                        var.screen.blit(var.house, (self.hx, (3 - self.house) * 15 + self.hy + i * 30))
        else:
            if self.w == 84:
                var.screen.blit(var.hotel, (self.hx + 27, self.hy))
            elif self.w == 134:
                var.screen.blit(var.hotel, (self.hx, self.hy + 27))

class Player:
    def __init__(self):
        self.moneys = [500, 100, 50] * 2 + [20] * 6 + [10, 5, 1] * 5
        self.properties = []
        self.dies = [(0, 0)] * 3
        self.index = 20
        self.targetindex = 20
        self.lasttarget = pygame.time.get_ticks()
        self.lastindex = 20
        self.last_go = 20
        self.switchable = True
        self.injail = False
        self.free_parking = False
    def get_index(self):
        self.index %= 40
        if self.targetindex != self.index:
            current = pygame.time.get_ticks()
            if current - self.lasttarget >= 200:
                self.targetindex += 1
                self.targetindex %= 40
                self.lasttarget = current
        if self.last_go < 20 and self.index > 20:
            self.moneys.extend([100, 100])
        self.last_go = self.index
        index = self.targetindex
        ii = index // 10
        if index % 10 != 0:
            num = index % 10
            if ii == 0:
                x = (num - 1) * 84 + 176
                y = 67
            elif ii == 1:
                x = 957
                y = (num - 1) * 84 + 176
            elif ii == 2:
                x = 1024 - num * 84 - 92
                y = 957
            elif ii == 3:
                x = 67
                y = 1024 - num * 84 - 92
        else:
            if ii in (0, 3):
                x = 67
            else:
                x = 957
            if ii in (0, 1):
                y = 67
            else:
                y = 957
        return x, y
    def update_dies(self, points1, points2):
        del self.dies[0]
        self.dies.append((points1, points2))
        if points1 == points2:
            if self.injail:
                self.injail = False
            else:
                self.switchable = False
    def draw_chess(self):
        x, y = self.get_index()
        ex, ey = var.computer.get_index()
        if x == ex and y == ey:
            y -= 20
        pygame.draw.circle(var.screen, (0, 180, 0), (x, y), 20, 0)
        pygame.draw.circle(var.screen, (0, 255, 0), (x, y), 7, 0)
    def format_pay(self, price, m):
        _500 = _100 = _50 = _20 = _10 = _5 = _1 = 0
        if m > 500:
            _500 = price // 500
            price -= _500 * 500
        if m > 100:
            _100 = price // 100
            price -= _100 * 100
        if m > 50:
            _50 = price // 50
            price -= _50 * 50
        if m > 20:
            _20 = price // 20
            price -= _20 * 20
        if m > 10:
            _10 = price // 10
            price -= _10 * 10
        if m > 5:
            _5 = price // 5
            price -= _5 * 5
        if m > 1:
            _1 = price // 1
        return [_500, _100, _50, _20, _10, _5, _1]
    def transform_money(self, money):
        if money in self.moneys:
            self.moneys.remove(money)
            if money == 500:
                self.moneys.extend([100] * 5)
            elif money == 100:
                self.moneys.extend([50] * 2)
            elif money == 50:
                self.moneys.extend([20] * 2 + [10])
            elif money == 20:
                self.moneys.extend([10] * 2)
            elif money == 10:
                self.moneys.extend([5] * 2)
            elif money == 5:
                self.moneys.extend([1] * 5)
            elif money == 1:
                self.moneys.extend([1])
                return False
            return True
        return False
    def pay(self, price):
        if price <= sum(self.moneys):
            orig = price
            _500, _100, _50, _20, _10, _5, _1 = self.format_pay(price, 1000)
            l = locals()
            moneys = [500, 100, 50, 20, 10, 5, 1]
            for m in moneys:
                num = l['_%d' % m]
                if self.moneys.count(m) >= num:
                    for i in range(num):
                        self.moneys.remove(m)
                    orig -= num * m
                else:
                    n = self.moneys.count(m)
                    for i in range(n):
                        self.moneys.remove(m)
                    orig -= n * m
                    _500, _100, _50, _20, _10, _5, _1 = self.format_pay(price - n * m, m)
                    l = locals()
            if orig == 0:
                return True
            if self.transform_money(sorted(self.moneys)[0]):
                return self.pay(orig)
        return False
    def get(self, price):
        _500, _100, _50, _20, _10, _5, _1 = self.format_pay(price, 1000)
        l = locals()
        moneys = [500, 100, 50, 20, 10, 5, 1]
        for m in moneys:
            num = l['_%d' % m]
            self.moneys.extend([m] * num)

class Computer(Player):
    def draw_chess(self):
        x, y = self.get_index()
        ex, ey = var.player.get_index()
        if x == ex and y == ey:
            y += 20
        pygame.draw.circle(var.screen, (180, 0, 0), (x, y), 20, 0)
        pygame.draw.circle(var.screen, (255, 0, 0), (x, y), 7, 0)

class Bank:
    def __init__(self):
        self.community_chests = 2

class Die:
    def __init__(self, x, y):
        self.faces = 6
        self.points = 6
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.lastthrow = None
        self.lastupdate = None
        self.ok = False
        self.state = True
    def throw(self):
        current = pygame.time.get_ticks()
        self.lastthrow = current
        self.lastupdate = current
    def circle(self, x, y):
        pygame.draw.circle(var.screen, (0, 0, 0), (x, y), 7, 0)
    def submit(self):
        res = self.ok
        self.ok = False
        return res
    def draw(self):
        if self.lastthrow is None:
            var.screen.blit(var.dice_s[self.points - 1], (self.x - 25, self.y - 25))
        else:
            if self.state:
                var.screen.blit(var.dice_s[self.points - 1], (self.x - 25, self.y - 25))
            else:
                var.screen.blit(var.dices[self.points - 1], (self.x - 25, self.y - 25))
    def update(self):
        if self.lastthrow is not None:
            current = pygame.time.get_ticks()
            if current - self.lastupdate >= 100:
                self.points = random.randint(1, self.faces)
                self.state = not self.state
                self.lastupdate = current
            if current - self.lastthrow >= 1000:
                self.lastthrow = None
                self.ok = True

norent = [None] * 7
def init_cards():
    names = ['FREE PARKING', 'KENTUCKY AVENUE',
             'CHANCE', 'INDIANA AVENUE',
             'ILLINOIS AVENUE', 'B.&O. RAILBOAD',
             'ATLANTIC AVENUE', 'VENTNOR AVENUE',
             'WATER WORKS', 'MARVIN GARDENS',
             'GO TO JAIL', 'PACIFIC AVENUE',
             'NORTH CAROLINA AVENUE', 'COMMUNITY CHEST',
             'PENNSYLVANIA AVENUE', 'SHORT LINE',
             'CHANCE', 'PARK LANE',
             'LUXURY TAX', 'BOARDWALK',
             'GO', 'MEDITERRANEAN AVENUE',
             'COMMUNITY CHEST', 'BALTIC AVENUE',
             'INCOME TAX', 'READING RAILBOAD',
             'ORIENTAL AVENUE', 'CHANCE',
             'VERMONT AVENUE', 'CONNECTICUT AVENUE',
             'IN JAIL', 'ST.CHARLES PLACE',
             'ELETRIC COMPANY', 'STATES AVENUE',
             'VIRGINIA AVENUE', 'PENSYSLVANIA RAILBOAD',
             'ST.JAMES PLACE', 'COMMUNITY CHEST',
             'TENNESSEE AVENUE', 'NEW YORK AVENUE']
    prices = [None, 220, None, 220, 240,
              200, 260, 260, 150, 280,
              None, 300, 300, None, 320,
              200, None, 350, -100, 400,
              None, 60, None, 60, -200,
              200, 100, None, 100, 120,
              None, 140, 150, 140, 160,
              200, 180, None, 180, 200]
    rents = [norent,
             [18, 36, 90, 250, 700, 875, 1050],
             norent,
             [18, 36, 90, 250, 700, 875, 1050],
             [20, 40, 100, 300, 750, 225, 1100],
             None,
             [22, 44, 110, 330, 800, 975, 1150],
             [22, 44, 110, 330, 800, 975, 1150],
             None,
             [24, 48, 120, 360, 850, 1025, 1200],
             norent,
             [26, 52, 130, 390, 900, 1100, 1275],
             [26, 52, 130, 390, 900, 1100, 1275],
             norent,
             [28, 56, 150, 450, 1000, 1200, 1400],
             None,
             norent,
             [35, 70, 175, 500, 1100, 1300, 1500],
             norent,
             [50, 100, 200, 600, 1400, 1700, 2000],
             norent,
             [2, 4, 10, 30, 90, 160, 250],
             norent,
             [4, 8, 20, 60, 180, 320, 450],
             norent,
             None,
             [6, 12, 30, 90, 270, 400, 550],
             norent,
             [6, 12, 30, 90, 270, 400, 550],
             [8, 16, 40, 100, 300, 450, 600],
             norent,
             [10, 20, 50, 150, 450, 625, 750],
             None,
             [10, 20, 50, 150, 450, 625, 750],
             [12, 24, 60, 180, 500, 700, 900],
             None,
             [14, 28, 70, 200, 550, 750, 950],
             norent,
             [14, 28, 70, 200, 550, 750, 950],
             [16, 32, 80, 220, 600, 800, 1000]]
    types = [None, 1, None, 1, 1, 9, 2, 2, 10, 2,
             None, 3, 3, None, 3, 9, None, 4, None, 4,
             None, 5, None, 5, None, 9, 6, None, 6, 6,
             None, 7, 10, 7, 7, 9, 8, None, 8, 8]
    for i in range(40):
        var.cards.append(Card(names[i], prices[i], rents[i], types[i], i))

def update():
    if var.pos == 'game':
        game.update_game(var)
    elif var.pos == 'mortgage':
        mortgage.update_mortgage(var)
    elif var.pos == 'win: player':
        var.screen.blit(var.screenshot, (0, 0))
        var.screen.blit(var.shadow, (0, 482))
        fill_text(var.screen, var.font_fangsong40, 'PLAYER WINS!', (762, 487), center=True, shadow=True)
    elif var.pos == 'win: computer':
        var.screen.blit(var.screenshot, (0, 0))
        var.screen.blit(var.shadow, (0, 482))
        fill_text(var.screen, var.font_fangsong40, 'EMMM...COMPUTER WINS', (762, 487), center=True, shadow=True)

def handle_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit
    if var.pos == 'game':
        game.handle_event_game(var, event)

var.player = Player()
var.computer = Computer()
var.now = var.player
var.bank = Bank()
var.cards = []
var.skipable = False
var.canset = False

var.mort_price = 0
var.now_selecting = None
var.window = None

var.buttons = []
var.die1 = Die(390, 487)
var.die2 = Die(584, 487)
var.die_shadow = pygame.Surface((300, 150)).convert_alpha()
var.die_shadow.fill((0, 0, 0, 100))

var.screenshot = var.screen.copy()
var.shadow = pygame.Surface((1624, 60)).convert_alpha()
var.shadow.fill((0, 0, 0, 100))

init_cards()

var.turns = 0
var.pos = 'game'

while True:
    update()
    for event in pygame.event.get():
        handle_event(event)
    pygame.display.update()
    var.fpsclock.tick(30)
