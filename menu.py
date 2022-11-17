# reqs
import pygame as pg

# local
from settings import *
from timer import Timer


class Menu:
    def __init__(self, player, toggle_menu_func):
        self.player = player
        self.toggle_menu = toggle_menu_func
        self.font = pg.font.Font('font/LycheeSoda.ttf', MENU_FONT_SIZE)

        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        # options index < the following means sellable; options index >= means buy only
        self.sell_index_line = len(self.player.item_inventory) - 1
        self.sell_text = self.font.render('sell', False, SELL_COLOR)
        self.buy_text = self.font.render('buy', False, BUY_COLOR)
        self.setup()

        # navigation
        self.menu_index = 0
        self.timer = Timer(INPUT_COOLDOWN)


    def setup(self):
        # create text surfaces
        self.text_surfs = []
        self.total_height = 0

        for item_index, item in enumerate(self.options):
            if item_index <= self.sell_index_line:
                text_surf = self.font.render(item, False, MENU_FONT_COLOR)
            else:
                text_surf = self.font.render(f'{item} seeds', False, MENU_FONT_COLOR)
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + MENU_PAD * 2  # spacing within categories

        self.total_height += (len(self.text_surfs) - 1) * MENU_SPACE # spacing between categories
        self.menu_top = (HEIGHT - self.total_height) / 2
        self.main_rect = pg.Rect((WIDTH - MENU_WIDTH) / 2, self.menu_top, MENU_WIDTH, self.total_height)


    def input(self):
        keys = pg.key.get_pressed()
        self.timer.update()

        if keys[pg.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pg.K_DOWN]:
                self.timer.activate()
                self.menu_index += 1
                if self.menu_index > len(self.options) - 1: self.menu_index = 0                
            elif keys[pg.K_UP]:
                self.timer.activate()
                self.menu_index -= 1
                if self.menu_index < 0: self.menu_index = len(self.options) - 1  
            
            if keys[pg.K_RETURN]:
                self.timer.activate()
                current_item = self.get_item(self.menu_index)
                if self.to_sell(self.menu_index):
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.bank_balance += SALE_PRICES[current_item]
                else:
                    if self.player.bank_balance >= SALE_PRICES[current_item]:
                        self.player.seed_inventory[current_item] += 1
                        self.player.bank_balance -= SALE_PRICES[current_item]
                        

    def show_entry(self, win, text_surf, amount, top, to_sell, is_selected):
        
        # bg
        bg_rect = pg.Rect(self.main_rect.left, top, MENU_WIDTH, text_surf.get_height() + MENU_PAD * 2)
        pg.draw.rect(win, MENU_BG_COLOR, bg_rect, 0, CORNER_RADIUS)

        # text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + TEXT_PAD, bg_rect.centery))
        win.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, f"{SELL_COLOR if to_sell else BUY_COLOR}")
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - TEXT_PAD, bg_rect.centery))
        win.blit(amount_surf, amount_rect)

        # selection
        if is_selected:
            pg.draw.rect(win, MENU_BORDER_COLOR, bg_rect, MENU_BORDER, CORNER_RADIUS)

            # display next to bank balance left: Buy or sell, right: amount +/-
            self.show_bank(win, to_sell)
            

    def show_bank(self, win, to_sell):
        text_surf = self.font.render(f'${self.player.bank_balance}', False, SELL_COLOR)
        text_rect = text_surf.get_rect(midbottom = (WIDTH / 2, HEIGHT - 50))
        pg.draw.rect(win, MENU_BG_COLOR, text_rect.inflate(8, 3), 0, CORNER_RADIUS)
        win.blit(text_surf, text_rect)

        if to_sell:
            # win.blit(self.sell_text, (text_rect.left - 100, text_rect.top))
            price_text = self.font.render(f'+ ${SALE_PRICES[self.get_item(self.menu_index)]}', False, SELL_COLOR)            

        else:
            # win.blit(self.buy_text, (text_rect.left - 100, text_rect.top))
            price_text = self.font.render(f'- ${SALE_PRICES[self.get_item(self.menu_index)]}', False, BUY_COLOR)
        win.blit(price_text, (text_rect.right + 30, text_rect.top))

    def to_sell(self, row_index):
        # return true if index = sell item, else it's a buy item
        return True if row_index <= self.sell_index_line else False

    
    def is_selected(self, row_index):
        # True if menu item is selected
        return True if row_index == self.menu_index else False

    
    def get_item(self, row_index):
        return self.options[row_index]


    def draw(self, win):
        # bank_balance is drawn via show_entry
        for row_index, text_surf in enumerate(self.text_surfs):

            # new line
            top = self.main_rect.top + row_index * (text_surf.get_height() + MENU_PAD * 2 + MENU_SPACE)

            # is list item for sale or for purchase?
            to_sell = self.to_sell(row_index)
            if to_sell:
                amount = self.player.item_inventory[self.get_item(row_index)]
            else:
                amount = self.player.seed_inventory[self.get_item(row_index)]

            # ship it
            self.show_entry(win, text_surf, amount, top, to_sell, self.is_selected(row_index))