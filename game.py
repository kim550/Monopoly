import pygame
import random

from functions import *
import mortgage

def draw_board(var):
    var.screen.blit(var.board, (0, 0))
    var.player.draw_chess()
    var.computer.draw_chess()

def draw_money(var, x, y):
    origx = x
    nowx = x
    n = 0
    for m in [500, 100, 50, 20, 10, 5, 1]:
        num = min(var.player.moneys.count(m), 3)
        for i in range(num):
            var.screen.blit(var.moneys[m], (nowx, y + (num - i) * 10))
        fill_text(var.screen, var.font_simhei22, '×%s' % var.player.moneys.count(m), (nowx + 205, y + 95), shadow=True)
        if nowx == origx:
            nowx += 300
            n = num
        else:
            nowx -= 300
            y += max(n, num) * 10 + 120
            n = 0
            
def draw_assets(var):
    pygame.draw.line(var.screen, (0, 0, 0), (1024, 0), (1024, 1024), 2)
    pygame.draw.line(var.screen, (0, 0, 0), (1028, 0), (1028, 1024), 2)
    text = var.font_fangsong40.render('TOTAL ASSETS: M%s' % sum(var.player.moneys), True, (0, 0, 0))
    pygame.draw.line(text, (0, 0, 0), (278, 20), (300, 20), 1)
    pygame.draw.line(text, (0, 0, 0), (278, 24), (300, 24), 1)
    var.screen.blit(text, (1040, 10))
    draw_money(var, 1040, 50)

def draw_deal(var):
    card = var.cards[var.player.index]
    if card.owner == None:
        if is_place(var.player.index) or is_railboad(var.player.index) or is_utility(var.player.index):
            text = var.font_fangsong35.render('PRICE: M%s' % card.price, True, (0, 0, 0))
            pygame.draw.line(text, (0, 0, 0), (125, 17), (142, 17), 1)
            pygame.draw.line(text, (0, 0, 0), (125, 20), (142, 20), 1)
            var.screen.blit(text, (1237, 750))
            if sum(var.player.moneys) >= card.price:
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('BUY IT!', var.font_fangsong30, 1326, 870, 120, 50, True,
                                          lambda: Callbacks.btn_buy_it(var.cards[var.player.index], var.player)))
                    var.buttons.append(Button('SKIP IT', var.font_fangsong30, 1326, 970, 120, 50, True, Callbacks.btn_skip_it))
            else:
                fill_text(var.screen, var.font_fangsong35, 'YOU CAN\'T AFFORD THE COST.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
            if var.canset:
                var.skipable = True
            var.player.lastindex = var.player.index
        elif card.price is not None and card.price < 0:
            text = var.font_fangsong35.render('PRICE: M%s' % -card.price, True, (0, 0, 0))
            pygame.draw.line(text, (0, 0, 0), (125, 17), (142, 17), 1)
            pygame.draw.line(text, (0, 0, 0), (125, 20), (142, 20), 1)
            var.screen.blit(text, (1237, 750))
            if sum(var.player.moneys) >= -card.price:
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('PAY FOR THE TAX', var.font_fangsong30, 1326, 870, 250, 50, True,
                                          lambda: Callbacks.btn_pay_for_the_tax(var.cards[var.player.index])))
            else:
                fill_text(var.screen, var.font_fangsong35, 'YOU CAN\'T AFFORD THE TAX.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('TO MORTGAGE', var.font_fangsong30, 1326, 970, 250, 50, True, lambda: Callbacks.btn_to_mortgage(-card.price)))
            var.player.lastindex = var.player.index
        elif card.name == 'COMMUNITY CHEST':
            if var.bank.community_chests > 0:
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('GET COMMUNITY CHEST', var.font_fangsong30, 1326, 770, 300, 50, True,
                                          lambda: Callbacks.btn_get_community_chest(card)))
            elif card.turns != var.turns:
                fill_text(var.screen, var.font_fangsong35, 'THERE IS NO COMMUNITY CHEST LEFT.', (1326, 770), color=(255, 0, 0), center=True, shadow=True)
                text = var.font_fangsong35.render('YOU CAN GET M%s INSTEAD.' % 50, True, (0, 0, 0))
                pygame.draw.line(text, (0, 0, 0), (215, 17), (232, 17), 1)
                pygame.draw.line(text, (0, 0, 0), (215, 20), (232, 20), 1)
                var.screen.blit(text, (1100, 850))
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('GET THE MONEY', var.font_fangsong30, 1326, 970, 250, 50, True, Callbacks.btn_get_the_money))
            var.player.lastindex = var.player.index
        elif card.name == 'GO TO JAIL':
            if var.player.index != var.player.lastindex:
                var.buttons.append(Button('GO TO JAIL', var.font_fangsong30, 1326, 970, 250, 50, True, Callbacks.btn_go_to_jail))
            var.player.lastindex = var.player.index
        elif card.name == 'CHANCE':
            fill_text(var.screen, var.font_fangsong35, 'NOW, JUST SKIP IT.', (1326, 770), color=(255, 0, 0), center=True, shadow=True)
            if var.player.index != var.player.lastindex:
                var.buttons.append(Button('SKIP IT', var.font_fangsong30, 1326, 870, 120, 50, True, Callbacks.btn_skip_it))
            if var.canset:
                var.skipable = True
            var.player.lastindex = var.player.index
        elif card.name == 'IN JAIL':
            if var.player.index != var.player.lastindex:
                var.buttons.append(Button('SKIP IT', var.font_fangsong30, 1326, 870, 120, 50, True, Callbacks.btn_skip_it))
            if var.canset:
                var.skipable = True
            var.player.lastindex = var.player.index
        elif card.name == 'FREE PARKING':
            fill_text(var.screen, var.font_fangsong35, 'YOU ARE NOW IN FREE PARKING.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
            if var.player.index != var.player.lastindex:
                var.player.free_parking = True
            var.player.lastindex = var.player.index
    elif card.owner == var.player:
        if is_place(var.player.index) and card.turns != var.turns:
            price = ((var.player.index // 10 + 2) % 4 + 1) * 50
            text = var.font_fangsong35.render('PRICE: M%s' % price, True, (0, 0, 0))
            pygame.draw.line(text, (0, 0, 0), (125, 17), (142, 17), 1)
            pygame.draw.line(text, (0, 0, 0), (125, 20), (142, 20), 1)
            var.screen.blit(text, (1237, 750))
            if card.house < 5:
                if sum(var.player.moneys) >= price:
                    if var.player.index != var.player.lastindex:
                        var.buttons.append(Button('BUILD A HOUSE', var.font_fangsong30, 1326, 870, 240, 50, True,
                                              lambda: Callbacks.btn_build_a_house(var.cards[var.player.index], price)))
                        var.buttons.append(Button('SKIP IT', var.font_fangsong30, 1326, 970, 120, 50, True, Callbacks.btn_skip_it))
                else:
                    fill_text(var.screen, var.font_fangsong35, 'YOU CAN\'T AFFORD THE COST.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
            else:
                fill_text(var.screen, var.font_fangsong35, 'THERE CAN\'T BE MORE HOUSES.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
            if var.canset:
                var.skipable = True
            var.player.lastindex = var.player.index
        if is_railboad(var.player.index) or is_utility(var.player.index):
            if var.player.index != var.player.lastindex:
                var.buttons.append(Button('SKIP IT', var.font_fangsong30, 1326, 870, 120, 50, True, Callbacks.btn_skip_it))
            if var.canset:
                var.skipable = True
            var.player.lastindex = var.player.index
    else:
        if is_place(var.player.index):
            price = 0
            if card.house == 0:
                price = card.rent[0]
                fill_text(var.screen, var.font_fangsong35, 'OPEN SPACE', (1326, 750), color=(255, 0, 0), center=True, shadow=True)
            else:
                price = card.rent[card.house + 1]
                fill_text(var.screen, var.font_fangsong35, '%s HOUSE%s' % (card.house, '' if card.house == 1 else 'S'), (1326, 750), color=(255, 0, 0),
                          center=True, shadow=True)
            text = var.font_fangsong35.render('PRICE: M%s' % price, True, (0, 0, 0))
            pygame.draw.line(text, (0, 0, 0), (125, 17), (142, 17), 1)
            pygame.draw.line(text, (0, 0, 0), (125, 20), (142, 20), 1)
            var.screen.blit(text, (1237, 810))
            if sum(var.player.moneys) >= price:
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('PAY FOR THE RENT', var.font_fangsong30, 1326, 920, 250, 50, True,
                                          lambda: Callbacks.btn_pay_for_the_rent(price)))
            else:
                fill_text(var.screen, var.font_fangsong35, 'YOU CAN\'T AFFORD THE RENT.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('TO MORTGAGE', var.font_fangsong30, 1326, 970, 250, 50, True, lambda: Callbacks.btn_to_mortgage(price)))
            var.player.lastindex = var.player.index
        elif is_railboad(var.player.index):
            num = len(list(filter(lambda prop: prop.card.type == 9, var.computer.properties)))
            price = [0, 25, 50, 100, 200][num]
            fill_text(var.screen, var.font_fangsong35, 'THE COMPUTER OWNED %s RAILBOAD%s.' % (num, '' if num == 1 else 'S'), (1326, 750), color=(255, 0, 0),
                      center=True, shadow=True)
            text = var.font_fangsong35.render('PRICE: M%s' % price, True, (0, 0, 0))
            pygame.draw.line(text, (0, 0, 0), (125, 17), (142, 17), 1)
            pygame.draw.line(text, (0, 0, 0), (125, 20), (142, 20), 1)
            var.screen.blit(text, (1237, 810))
            if sum(var.player.moneys) >= price:
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('PAY FOR THE RENT', var.font_fangsong30, 1326, 920, 250, 50, True,
                                          lambda: Callbacks.btn_pay_for_the_rent(price)))
            else:
                fill_text(var.screen, var.font_fangsong35, 'YOU CAN\'T AFFORD THE RENT.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('TO MORTGAGE', var.font_fangsong30, 1326, 970, 250, 50, True, lambda: Callbacks.btn_to_mortgage(price)))
            var.player.lastindex = var.player.index
        elif is_utility(var.player.index):
            num = len(list(filter(lambda prop: prop.card.type == 10, var.computer.properties)))
            if var.player.index != var.player.lastindex:
                times = 4 if num == 1 else 10
                var.player.temp = (random.randint(1, 6) + random.randint(1, 6)) * times
            price = var.player.temp
            fill_text(var.screen, var.font_fangsong35, 'THE var.computer OWNED %s UTILIT%s.' % (num, 'Y' if num == 1 else 'IES'), (1326, 750), color=(255, 0, 0),
                      center=True, shadow=True)
            text = var.font_fangsong35.render('PRICE: M%s' % price, True, (0, 0, 0))
            pygame.draw.line(text, (0, 0, 0), (125, 17), (142, 17), 1)
            pygame.draw.line(text, (0, 0, 0), (125, 20), (142, 20), 1)
            var.screen.blit(text, (1237, 810))
            if sum(var.player.moneys) >= price:
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('PAY FOR THE RENT', var.font_fangsong30, 1326, 920, 250, 50, True,
                                          lambda: Callbacks.btn_pay_for_the_rent(price)))
            else:
                fill_text(var.screen, var.font_fangsong35, 'YOU CAN\'T AFFORD THE RENT.', (1326, 870), color=(255, 0, 0), center=True, shadow=True)
                if var.player.index != var.player.lastindex:
                    var.buttons.append(Button('TO MORTGAGE', var.font_fangsong30, 1326, 970, 250, 50, True, lambda: Callbacks.btn_to_mortgage(price)))
            var.player.lastindex = var.player.index
    var.canset = False

def draw_deal_frame(var):
    pygame.draw.line(var.screen, (0, 0, 0), (1024, 660), (1624, 660), 2)
    pygame.draw.line(var.screen, (0, 0, 0), (1024, 664), (1624, 664), 2)
    fill_text(var.screen, var.font_fangsong40, format_card(var.player.index), (1326, 690), center=True, shadow=True)
    draw_deal(var)

def draw_units(var):
    for button in var.buttons:
        button.update()
        button.draw()
    for card in var.cards:
        if card.owner is not None:
            card.draw()
    var.screen.blit(var.die_shadow, (362, 437))
    var.die1.update()
    var.die2.update()
    var.die1.draw()
    var.die2.draw()

def update_board(var):
    draw_board(var)
    draw_assets(var)
    if var.now == var.player and var.die1.lastthrow is None and var.die2.lastthrow is None and var.player.index == var.player.targetindex:
        draw_deal_frame(var)
    draw_units(var)

def computer_turn(var):
    var.computer.index %= 40
    card = var.cards[var.computer.index]
    if card.owner is None:
        if is_place(var.computer.index) or is_railboad(var.computer.index) or is_utility(var.computer.index):
            if sum(var.computer.moneys) >= card.price:
                var.computer.pay(card.price)
                card.owner = var.computer
                card.turns = var.turns
                var.computer.properties.append(Property(card))
        elif card.price is not None and card.price < 0:
            if sum(var.computer.moneys) >= -card.price:
                var.computer.pay(-card.price)
        elif card.name == 'COMMUNITY CHEST':
            if var.bank.community_chests > 0:
                var.computer.properties.append(Property(card))
            else:
                var.computer.moneys.append(50)
        elif card.name == 'GO TO JAIL':
            var.computer.injail = True
            var.computer.index = var.computer.lastindex = var.computer.last_go = var.computer.targetindex = 30
        elif card.name == 'FREE PARKING':
            var.computer.free_parking = True
    elif card.owner == var.player:
        if is_place(var.computer.index):
            price = card.rent[0] if card.house == 0 else card.rent[card.house + 1]
            if sum(var.computer.moneys) >= price:
                var.computer.pay(price)
                var.player.get(price)
            else:
                mortgage.mortgage_computer(var, price)
        elif is_utility(var.computer.index):
            num = len(list(filter(lambda prop: prop.card.type == 10, var.computer.properties)))
            times = 4 if num == 1 else 10
            price = (random.randint(1, 6) + random.randint(1, 6)) * times
            if sum(var.computer.moneys) >= price:
                var.computer.pay(price)
                var.player.get(price)
            else:
                mortgage.mortgage_computer(var, price)
        elif is_railboad(var.computer.index):
            num = len(list(filter(lambda prop: prop.card.type == 9, var.computer.properties)))
            price = [0, 25, 50, 100, 200][num]
            if sum(var.computer.moneys) >= price:
                var.computer.pay(price)
                var.player.get(price)
            else:
                mortgage.mortgage_computer(var, price)
    else:
        if is_place(var.computer.index):
            price = ((var.computer.index // 10 + 2) % 4 + 1) * 50
            if card.house < 5:
                if sum(var.computer.moneys) >= price + 200:
                    var.computer.pay(price)
                    card.house += 1
                elif sum(var.computer.moneys) >= price:
                    if random.randint(1, 4) == 1:
                        var.computer.pay(price)
                        card.house += 1

def update_game(var):
    var.screen.fill((230, 230, 230))
    if var.die1.submit() and var.die2.submit():
        index = var.die1.points + var.die2.points
        if var.now == var.player:
            var.player.update_dies(var.die1.points, var.die2.points)
            if not var.player.injail:
                var.player.index += index
                var.canset = True
            else:
                var.now = var.computer
        else:
            var.computer.update_dies(var.die1.points, var.die2.points)
            if not var.computer.injail:
                var.computer.index += index
            else:
                var.now = var.player
    if var.now == var.computer and var.computer.index == var.computer.targetindex and var.die1.lastthrow is None and var.die2.lastthrow is None:
        computer_turn(var)
        if var.computer.switchable:
            var.now = var.player
        else:
            var.die1.throw()
            var.die2.throw()
        var.computer.switchable = True
    update_board(var)

def handle_event_game(var, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if var.now == var.player:
            if not var.player.free_parking:
                if var.die1.lastthrow is None and var.die2.lastthrow is None:
                    if event.button in (1, 4, 5) and event.pos[0] < 1024:
                        if len(var.buttons) == 0:
                            var.die1.throw()
                            var.die2.throw()
                            var.turns += 1
                        elif var.skipable:
                            set_to_computer()
                            var.skipable = False
            else:
                set_to_computer()
                var.player.free_parking = False
