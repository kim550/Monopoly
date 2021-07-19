import pygame

var = None
def init(v):
    global var
    var = v

class Button:
    def __init__(self, text, font, x, y, width, height, center, callback):
        self.text = text
        self.font = font
        self.rect = pygame.Rect(0, 0, width, height)
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.x = x
            self.rect.y = y
        self.callback = callback
        self.color = 200
        self.textcolor = 0
        self.state = 0
        self.disabled = False
    def draw(self):
        pygame.draw.rect(var.screen, (self.color, self.color, self.color), self.rect, 0)
        pygame.draw.rect(var.screen, (100, 100, 100), self.rect, 1)
        fill_text(var.screen, self.font, self.text, self.rect.center, color=(self.textcolor, self.textcolor, self.textcolor), center=True, shadow=True)
    def update(self):
        if not self.disabled:
            mx, my = pygame.mouse.get_pos()
            b1, b2, b3 = pygame.mouse.get_pressed()
            if self.rect.collidepoint(mx, my):
                if b1:
                    n = 150
                    if self.color == 165 and self.state == 0:
                        self.state = 1
                        if self.callback:
                            self.callback()
                else:
                    n = 175
                    if self.color < n:
                        self.color += 5
                if self.color > n:
                    self.color -= 5
            else:
                if self.color < 200:
                    self.color += 5
            if self.textcolor > 0:
                self.textcolor -= 10
        else:
            if self.textcolor < 100:
                self.textcolor += 10

class Callbacks:
    @staticmethod
    def btn_buy_it(card, owner):
        if var.player.pay(card.price):
            var.player.properties.append(Property(card))
            card.owner = owner
            card.turns = var.turns
        set_to_computer()
    @staticmethod
    def btn_build_a_house(card, price):
        if var.player.pay(price):
            card.house += 1
        set_to_computer()
    @staticmethod
    def btn_pay_for_the_tax(card):
        var.player.pay(-card.price)
        set_to_computer()
    @staticmethod
    def btn_skip_it():
        set_to_computer()
    @staticmethod
    def btn_get_community_chest(card):
        var.player.properties.append(Property(card))
        var.bank.community_chests -= 1
        card.turns = var.turns
        set_to_computer()
    @staticmethod
    def btn_get_the_money():
        var.player.moneys.append(50)
        set_to_computer()
    @staticmethod
    def btn_pay_for_the_rent(price):
        var.player.pay(price)
        var.computer.get(price)
        set_to_computer()
    @staticmethod
    def btn_go_to_jail():
        var.player.injail = True
        var.player.index = var.player.lastindex = var.player.last_go = var.player.targetindex = 30
        set_to_computer()
    @staticmethod
    def btn_to_mortgage(mort):
        price = sum(var.player.moneys)
        for prop in var.player.properties:
            if prop.mort_value[0]:
                price += prop.card.price // 2
            for i in range(1, 6):
                if prop.mort_value[i]:
                    hp = ((prop.card.index // 10 + 2) % 4 + 1) * 50
                    price += hp
        if price >= mort:
            var.pos = 'mortgage'
            var.mort_price = mort - sum(player.moneys)
        else:
            var.pos = 'win: computer'
            var.screenshot = var.screen.copy()

class Property:
    def __init__(self, card):
        self.card = card
        self.colorlist = [None, (237, 27, 36), (254, 242, 0), (31, 178, 90), (0, 114, 187),
                          (149, 84, 52), (169, 225, 248), (217, 58, 148), (247, 148, 29)]
        self.color = 255
        self.shadow = 255
        self.selected = False
        self.pressed = False
        self.mort_value = None
    def draw(self, x, y):
        if self.selected:
            pygame.draw.rect(var.screen, (255, 255, 0), (x, y, 240, 435), 0)
        else:
            pygame.draw.rect(var.screen, (255, 255, self.color), (x, y, 240, 435), 0)
        pygame.draw.rect(var.screen, (self.shadow, self.shadow, self.shadow), (x + 7, y + 7, 226, 421), 0)
        pygame.draw.rect(var.screen, (0, 0, 0), (x + 7, y + 7, 226, 421), 2)
        if is_place(self.card.index):
            color = self.colorlist[self.card.type]
            pygame.draw.rect(var.screen, color, (x + 15, y + 15, 210, 75), 0)
            pygame.draw.rect(var.screen, (0, 0, 0), (x + 15, y + 15, 210, 75), 2)
            l = self.card.name.split()
            num = len(l)
            yy = (4 - num) * 12
            ty = y + 15 + yy
            for text in l:
                fill_text(var.screen, var.font_simhei22, text, (x + 120, ty), center=True)
                ty += 24
            if self.card.house == 0:
                fill_text(var.screen, var.font_fangsong30, 'OPEN SPACE', (x + 120, y + 120), color=(255, 0, 0), center=True, shadow=True)
            else:
                fill_text(var.screen, var.font_fangsong30, '%s HOUSE%s' % (self.card.house, '' if self.card.house == 1 else 'S'), (x + 120, y + 120),
                          color=(255, 0, 0), center=True, shadow=True)
            prompts = ['Rent',
                       'Rent with color set',
                       'Rent with 1 house',
                       'Rent with 2 houses',
                       'Rent with 3 houses',
                       'Rent with 4 houses',
                       'Rent with a hotel']
            ty = y + 180
            for i, prompt in enumerate(prompts):
                fill_text(var.screen, var.font_aerial26, prompt, (x + 15, ty))
                text = var.font_aerial26.render('M' + str(self.card.rent[i]), True, (0, 0, 0))
                pygame.draw.line(text, (0, 0, 0), (0, 5), (13, 6), 2)
                pygame.draw.line(text, (0, 0, 0), (0, 8), (13, 9), 2)
                var.screen.blit(text, (x + 225 - text.get_width(), ty))
                ty += 34
    def update(self, x, y):
        mx, my = pygame.mouse.get_pos()
        b1, b2, b3 = pygame.mouse.get_pressed()
        rect = pygame.Rect(x, y, 240, 435)
        if rect.collidepoint(mx, my):
            if b1:
                if not self.pressed:
                    self.selected = not self.selected
                    if self.selected:
                        var.now_selecting = self
                    else:
                        if var.now_selecting is self:
                            var.now_selecting = None
                        self.mort_value = None
                    self.pressed = True
                n = 55
            else:
                self.pressed = False
                n = 155
                if self.color < n:
                    self.color += 10
            if self.color > n:
                self.color -= 10
        else:
            if self.color < 255:
                self.color += 10
        if self.selected:
            if self.shadow > 240:
                self.shadow -= 5
        else:
            if self.shadow < 255:
                self.shadow += 5

def fill_text(surface, font, text, pos, color=(0, 0, 0), shadow=False, center=False, right=False, shadow_color=None):
    text1 = font.render(text, True, color)
    text_rect = text1.get_rect()
    if shadow:
        if shadow_color is None:
            text2 = font.render(text, True, (255 - color[0], 255 - color[1], 255 - color[2]))
        else:
            text2 = font.render(text, True, shadow_color)
        for p in [(pos[0] - 1, pos[1] - 1),
                  (pos[0] + 1, pos[1] - 1),
                  (pos[0] - 1, pos[1] + 1),
                  (pos[0] + 1, pos[1] + 1)]:
            if center:
                text_rect.center = p
            else:
                text_rect.x = p[0]
                text_rect.y = p[1]
            surface.blit(text2, text_rect)
    if center:
        text_rect.center = pos
    elif right:
        text_rect.right = pos[0]
        text_rect.y = pos[1]
    else:
        text_rect.x = pos[0]
        text_rect.y = pos[1]
    surface.blit(text1, text_rect)

def is_place(index):
    return index in [1, 3, 4, 6, 7, 9, 11, 12, 14, 17, 19, 21, 23, 26, 28, 29, 31, 33, 34, 36, 38, 39]

def is_railboad(index):
    return index in [5, 15, 25, 35]

def is_utility(index):
    return index in [8, 32]

def set_to_computer():
    if var.player.switchable:
        if not var.computer.free_parking:
            var.now = var.computer
            var.die1.throw()
            var.die2.throw()
        else:
            var.now = var.player
        var.computer.free_parking = False
    var.player.switchable = True
    var.buttons.clear()

def format_card(index):
    cards = ['FREE PARKING', 'KENTUCKY AVENUE',
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
    return cards[index]
