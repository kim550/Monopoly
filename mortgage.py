import pygame
import copy

from functions import *
import functions

WINDOW_CREATE = pygame.USEREVENT + 1
WINDOW_CLOSE = pygame.USEREVENT + 2

class Window:
    def __init__(self, var, x, y, width, height, color, title):
        self.var = var
        if x == -1:
            self.x = (self.var.screen.get_width() - width) // 2
        else:
            self.x = x
        if y == -1:
            self.y = (self.var.screen.get_height() - height) // 2
        else:
            self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width, self.height))
        self.shadow = self.var.screen.copy().convert_alpha()
        self.shadow.fill((0, 0, 0, 100))
        self.color = color
        self.title = title
        self.titletext = self.var.font_simhei30.render(self.title, True, (0, 0, 0))
        self.titletext_rect = self.titletext.get_rect()
        self.titletext_rect.center = (self.width // 2, 25)
        self.proc = None
        self.events = [pygame.event.Event(WINDOW_CREATE)]
        self.widgets = []
        self.move_mx = -1
        self.move_my = -1
        self.clear()
    def clear(self):
        self.surface.fill(self.color)
        pygame.draw.rect(self.surface, (255, 255, 255), (0, 0, self.width, 50), 0)
        pygame.draw.line(self.surface, (0, 0, 0), (0, 50), (self.width, 50), 1)
        self.surface.blit(self.titletext, self.titletext_rect)
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, self.width, self.height), 1)
    def blit(self, surf, pos):
        self.var.screen.blit(surf, pos)
    def draw(self):
        self.clear()
        for widget in self.widgets:
            widget.draw()
        self.blit(self.shadow, (0, 0))
        self.blit(self.surface, (self.x, self.y))
    def update(self):
        mx, my = pygame.mouse.get_pos()
        b1, b2, b3 = pygame.mouse.get_pressed()
        if b1:
            if self.move_mx == -1:
                xx = mx - self.x
                yy = my - self.y
                if 0 <= xx < self.width and 0 <= yy < 50:
                    self.move_mx = mx
                    self.move_my = my
            else:
                self.x += (mx - self.move_mx)
                self.y += (my - self.move_my)
                self.move_mx = mx
                self.move_my = my
        else:
            self.move_mx = -1
        for widget in self.widgets:
            widget.update()
        for event in pygame.event.get():
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                pos = event.pos
                event.pos = (event.pos[0] - self.x, event.pos[1] - self.y)
                if not (0 <= event.pos[0] < self.width and 0 <= event.pos[1] < self.height):
                    event.pos = pos
                    pygame.event.post(event)
                    continue
                self.events.append(event)
                continue
            elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self.events.append(event)
                continue
            pygame.event.post(event)
    def get_events(self):
        events = self.events.copy()
        self.events.clear()
        return events
    def mouse_get_pos(self):
        mx, my = pygame.mouse.get_pos()
        return max(min(mx - self.x, self.width - 1), 0), max(min(my - self.y, self.height - 1), 0)
    def mouse_get_pressed(self):
        return pygame.mouse.get_pressed()
    def close(self):
        self.events.append(pygame.event.Event(WINDOW_CLOSE))

class Label:
    def __init__(self, var, window, x, y, font, text, color=(0, 0, 0), center=False):
        self.var = var
        self.window = window
        self.surface = self.window.surface
        self.font = font
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.center = center
        self.window.widgets.append(self)
    def draw(self):
        fill_text(self.surface, self.font, self.text, (self.x, self.y), color=self.color, center=self.center)
    def update(self): pass

class Button:
    def __init__(self, var, window, x, y, text, callback):
        self.var = var
        self.window = window
        self.surface = self.window.surface
        self.x = x
        self.y = y
        self.text = text
        self.img = self.var.font_fangsong30.render(self.text, True, (0, 0, 0))
        self.img_rect = self.img.get_rect()
        self.img_rect.centery = self.y + 20
        self.img_rect.left = self.x + 10
        self.whole = pygame.Rect(self.x, self.y, 20 + self.img.get_width(), 40)
        self.color = 255
        self.callback = callback
        self.disabled = False
        self.pressed = False
        self.window.widgets.append(self)
    def draw(self):
        if self.disabled:
            pygame.draw.rect(self.surface, (230, 230, 230), self.whole, 0)
            color = (100, 100, 100)
        else:
            pygame.draw.rect(self.surface, (self.color, self.color, self.color), self.whole, 0)
            color = (0, 0, 0)
        pygame.draw.rect(self.surface, color, self.whole, 1)
        self.surface.blit(self.img, self.img_rect)
    def disable(self):
        self.disabled = True
        self.img = self.var.font_fangsong30.render(self.text, True, (100, 100, 100))
    def enable(self):
        self.disabled = False
        self.img = self.var.font_fangsong30.render(self.text, True, (0, 0, 0))
    def update(self):
        if not self.disabled:
            mx, my = self.window.mouse_get_pos()
            b1, b2, b3 = self.window.mouse_get_pressed()
            if self.whole.collidepoint(mx, my):
                if b1:
                    self.pressed = True
                    n = 205
                else:
                    if self.pressed:
                        if self.callback:
                            self.callback(self)
                        self.pressed = False
                    n = 230
                    if self.color < n:
                        self.color += 5
                if self.color > n:
                    self.color -= 5
            else:
                self.pressed = False
                if self.color < 255:
                    self.color += 5

class CheckButton:
    def __init__(self, var, window, x, y, text, callback):
        self.var = var
        self.window = window
        self.surface = self.window.surface
        self.x = x
        self.y = y
        self.text = text
        self.img = self.var.font_fangsong30.render(self.text, True, (0, 0, 0))
        self.img_rect = self.img.get_rect()
        self.img_rect.centery = self.y + 10
        self.img_rect.left = self.x + 28
        self.rect = pygame.Rect(self.x + 5, self.y + 5, 20, 20)
        self.whole = pygame.Rect(self.x, self.y, 28 + self.img.get_width(), 30)
        self.color = 255
        self.callback = callback
        self.disabled = False
        self.pressed = False
        self.selected = False
        self.window.widgets.append(self)
    def draw(self):
        pygame.draw.rect(self.surface, (self.color, self.color, self.color), self.rect, 0)
        if self.disabled:
            color = (100, 100, 100)
        else:
            color = (0, 0, 0)
        pygame.draw.rect(self.surface, color, self.rect, 1)
        if self.selected:
            pygame.draw.line(self.surface, color, (self.x + 7, self.y + 15), (self.x + 12, self.y + 20), 2)
            pygame.draw.line(self.surface, color, (self.x + 12, self.y + 20), (self.x + 22, self.y + 10), 2)
        self.surface.blit(self.img, self.img_rect)
    def disable(self):
        self.disabled = True
        self.img = self.var.font_fangsong30.render(self.text, True, (100, 100, 100))
    def enable(self):
        self.disabled = False
        self.img = self.var.font_fangsong30.render(self.text, True, (0, 0, 0))
    def update(self):
        if not self.disabled:
            mx, my = self.window.mouse_get_pos()
            b1, b2, b3 = self.window.mouse_get_pressed()
            if self.rect.collidepoint(mx, my):
                if b1:
                    self.pressed = True
                    n = 205
                else:
                    if self.pressed:
                        self.selected = not self.selected
                        if self.callback:
                            self.callback(self)
                        self.pressed = False
                    n = 230
                    if self.color < n:
                        self.color += 5
                if self.color > n:
                    self.color -= 5
            else:
                self.pressed = False
                if self.color < 255:
                    self.color += 5

def draw_properties(var):
    x = 50
    y = 50
    for prop in var.player.properties:
        if is_place(prop.card.index):
            if var.window is None:
                prop.update(x, y)
            prop.draw(x, y)
        x += 270

cbs = []
def windowproc(window):
    card = window.var.now_selecting.card
    for event in window.get_events():
        if event.type == WINDOW_CREATE:
            Label(window.var, window, 200, 100, window.var.font_fangsong40, card.name, center=True)
            Label(window.var, window, 200, 160, window.var.font_fangsong35, 'What do you want', center=True)
            Label(window.var, window, 200, 200, window.var.font_fangsong35, 'to mortgage?', center=True)

            def callback_ckbtn(cb, card):
                if cb.text == 'hotel':
                    if cb.selected:
                        for i in range(1, 5):
                            cbs[i].enable()
                    else:
                        for i in range(0, 5):
                            cbs[i].disable()
                            cbs[i].selected = False
                elif cb.text == 'house':
                    l = list(filter(lambda cb: cb.text == 'house' and cb.selected, cbs))
                    if cb.selected:
                        if len(l) == min(4, card.house):
                            cbs[0].enable()
                    else:
                        if len(l) < min(4, card.house):
                            cbs[0].disable()
                            cbs[0].selected = False

            texts = ['open space', *['house'] * 4, 'hotel']
            for i, text in enumerate(texts):
                cbs.append(CheckButton(window.var, window, 100, 260 + i * 40, text, lambda cb: callback_ckbtn(cb, card)))
            h = card.house
            if h == 5:
                for i in range(5):
                    cbs[i].disable()
            elif 1 <= h <= 4:
                cbs[5].disable()
                for i in range(4 - h):
                    cbs[4 - i].disable()
                cbs[0].disable()
            elif h == 0:
                for i in range(1, 6):
                    cbs[i].disable()
            else:
                for i in range(6):
                    cbs[i].disable()

            Button(window.var, window, 155, 520, '  OK  ', lambda btn: window.close())

        elif event.type == WINDOW_CLOSE:
            if len(list(filter(lambda cb: not cb.disabled and cb.selected, cbs))) == 0:
                window.var.now_selecting.selected = False
            window.var.now_selecting.mort_value = list(map(lambda cb: cb.selected, cbs))
            cbs.clear()
            window.var.now_selecting = None
            window.var.window = None

def update_window(var):
    if var.now_selecting is not None:
        if var.window is None:
            var.window = Window(var, -1, -1, 400, 600, (230, 230, 230), 'Mortgage Details')
        var.window.update()
        var.window.draw()
        windowproc(var.window)

def calc_price(var):
    props = list(filter(lambda prop: prop.mort_value is not None, var.player.properties))
    price = 0
    for prop in props:
        if prop.mort_value[0]:
            price += prop.card.price // 2
        for i in range(1, 6):
            if prop.mort_value[i]:
                hp = ((prop.card.index // 10 + 2) % 4 + 1) * 50
                price += hp
    return price

def draw_mort_price(var):
    left = var.mort_price - calc_price(var)
    if left > 0:
        text = var.font_fangsong35.render('MONEY LEFT: M%s.' % left, True, (255, 0, 0))
        pygame.draw.line(text, (255, 0, 0), (216, 17), (232, 17), 1)
        pygame.draw.line(text, (255, 0, 0), (216, 20), (232, 20), 1)
        var.screen.blit(text, (1300, 920))
        var.buttons[0].disabled = True
    else:
        text = var.font_fangsong35.render('THE MONEY IS ENOUGH.', True, (0, 255, 0))
        var.screen.blit(text, (1250, 920))
        var.buttons[0].disabled = False

def draw_units(var):
    for button in var.buttons:
        if var.window is None:
            button.update()
        button.draw()

def mortgage_computer(var, price):
    left = price - sum(var.computer.moneys)
    money = 0
    for i in range(5, 0, -1):
        for prop in var.computer.properties:
            i = prop.card.index
            if is_place(i):
                if prop.card.house == i:
                    hp = ((i // 10 + 2) % 4 + 1) * 50
                    prop.card.house = 4
                    money += hp
        if money >= left:
            var.computer.get(money)
            return
    for prop in var.computer.properties[:]:
        i = prop.card.index
        if is_place(i):
            prop.card.owner = None
            var.computer.properties.remove(prop)
            money += prop.card.price // 2
    if money >= left:
        var.player.get(money)
        return
    else:
        var.pos = 'win: player'
        var.screenshot = var.screen.copy()

def btn_ok(var):
    global first
    first = True
    var.pos = 'game'
    props = list(filter(lambda prop: prop.mort_value is not None, var.player.properties))
    price = 0
    for prop in props[:]:
        prop.card.owner = None
        if prop.mort_value[0]:
            price += prop.card.price // 2
            var.player.properties.remove(prop)
        for i in range(1, 6):
            if prop.mort_value[i]:
                hp = ((prop.card.index // 10 + 2) % 4 + 1) * 50
                prop.card.house -= 1
                price += hp
    var.player.get(price)
    var.mort_price = 0
    var.now = var.player
    var.buttons.clear()
    var.player.lastindex = 0

first = True
def update_mortgage(var):
    global first, btns
    if first:
        var.buttons.clear()
        var.buttons.append(functions.Button('OK', var.font_fangsong30, 762, 952, 120, 50, True, lambda: btn_ok(var)))
        first = False
    var.screen.fill((0, 0, 100))
    draw_properties(var)
    draw_mort_price(var)
    draw_units(var)
    update_window(var)
