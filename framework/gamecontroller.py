import pygame
from framework.deck import Deck

class GameController(object):
    def __init__(self, display_width, display_height):
        self.deck = Deck()
        self.deck_pos =  (display_width - 150, (display_height / 2) - 43)
        self.background_image = pygame.transform.scale(pygame.image.load('images/card_background/background.jpg'), (display_width, display_height))
        self.cardback_image = pygame.transform.scale(pygame.image.load('images/Cards/cardBack_red2.png'), (70, 95))
        self.shuffling = False
        self.dealing = True
        self.shuffle_step = 1
        self.deal_step = 1
        self.dealing_card = None
        self.player1_cards = []
        self.player2_cards = []
        self.player1_deck_pos = (150, 30)
        self.player2_deck_pos = (150, display_height - 115)
        self.player1_battle_pos = (150, 140)
        self.player2_battle_pos = (150, display_height - 115 - 130)
        self.battle = False
        self.battle_step = 0
        self.player1_battle_card = None
        self.player2_battle_card = None
        self.display_battle = False
        self.battle_winner = None
        self.war = False
        self.collecting = False
        self.collecting_step = 1
        pass
    def act(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
        if self.dealing:
            deal_speed = 10
            if len(self.deck.cards) > 0 and not self.dealing_card:
                self.dealing_card = self.deck.cards.pop()
            elif self.dealing_card:
                if self.deal_step > deal_speed:
                    self.player1_cards.append(self.dealing_card)
                    self.deal_step = -1
                    self.dealing_card = None
                if self.deal_step < -(deal_speed):
                    self.player2_cards.append(self.dealing_card)
                    self.deal_step = 1
                    self.dealing_card = None

                if len(self.player1_cards) <= len(self.player2_cards) and self.deal_step > 0:
                    self.deal_step += 1
                elif len(self.player1_cards) > len(self.player2_cards) and self.deal_step < 0:
                    self.deal_step -= 1
            else:
                self.dealing = False
                self.battle = True

        if self.battle and self.battle_step == 0:
            self.battle_step = 1
            self.player1_battle_card = self.player1_cards.pop()
            self.player2_battle_card = self.player2_cards.pop()
        elif self.battle:
            self.battle_step += 1
            if self.battle_step == 20:
                self.display_battle = True
            elif self.battle_step == 45:
                if self.player1_battle_card.value > self.player2_battle_card.value:
                    self.battle_winner = 1
                elif self.player1_battle_card.value < self.player2_battle_card.value:
                    self.battle_winner = 2
                else:
                    self.war = True
                    self.battle = False
            if self.battle_step > 200:
                self.display_battle = False
                self.collecting_step = 1
                self.collecting = True
                self.battle = False
                self.battle_step = 0

        if self.collecting and self.collecting_step < 40:
            self.collecting_step += 1
        elif self.collecting:
            if self.battle_winner == 1:
                self.player1_cards.insert(0, self.player1_battle_card)
                self.player1_cards.insert(0, self.player2_battle_card)
            if self.battle_winner == 2:
                self.player2_cards.insert(0, self.player2_battle_card)
                self.player2_cards.insert(0, self.player1_battle_card)
            self.collecting = False
            self.battle = True
            self.battle_winner = None

        
    def draw(self, game_display, height, width):
        game_display.blit(self.background_image, (0, 0))
        if self.shuffling:
            half_size = int(len(self.deck.cards) / 2)
            if self.shuffle_step < 130:
                cut_pos = (width - 150 - self.shuffle_step + half_size, (height / 2) - 43 - half_size)
            else:
                cut_pos = (width - 150 - 130 + half_size, (height / 2) - 43 - half_size + self.shuffle_step - 130)
            for i in range(half_size):
                game_display.blit(self.cardback_image, (self.deck_pos[0] + i, self.deck_pos[1] - i))
            for i in range(half_size):
                game_display.blit(self.cardback_image, (cut_pos[0] + i, cut_pos[1] - i))
            self.shuffle_step += 2
        else:
            for i in range(len(self.deck.cards)):
                game_display.blit(self.cardback_image, (self.deck_pos[0] + i, self.deck_pos[1] - i))
            for i in range(len(self.player1_cards)):
                game_display.blit(self.cardback_image, (self.player1_deck_pos[0] + i, self.player1_deck_pos[1] - i))
            for i in range(len(self.player2_cards)):
                game_display.blit(self.cardback_image, (self.player2_deck_pos[0] + i, self.player2_deck_pos[1] - i))

        if self.dealing_card:
            increment = self.deal_step * 10
            if self.deal_step > 0:
                game_display.blit(self.cardback_image, (self.deck_pos[0] + i - increment, self.deck_pos[1] - i - increment))
            elif self.deal_step < 0:
                game_display.blit(self.cardback_image, (self.deck_pos[0] + i + increment, self.deck_pos[1] - i - increment))
        
        if self.battle and not self.display_battle:
            increment = self.battle_step * 6
            game_display.blit(self.cardback_image, (self.player1_deck_pos[0], self.player1_deck_pos[1] + increment))
            game_display.blit(self.cardback_image, (self.player2_deck_pos[0], self.player2_deck_pos[1] - increment))
       
        if self.display_battle:
            game_display.blit(self.player1_battle_card.image, self.player1_battle_pos)       
            game_display.blit(self.player2_battle_card.image, self.player2_battle_pos)       

        if self.collecting:
            increment = -(self.collecting_step * 9)
            if self.battle_winner == 2:
                increment = -(increment)
            game_display.blit(self.player1_battle_card.image, (self.player1_battle_pos[0], self.player1_battle_pos[1] + increment))      
            game_display.blit(self.player2_battle_card.image, (self.player2_battle_pos[0], self.player2_battle_pos[1] + increment))      

        text = pygame.font.Font('freesansbold.ttf', 20)
        text_surf = text.render(f'Player 1 ({len(self.player1_cards)})', True, (0, 0, 0))
        game_display.blit(text_surf, (5, 5))
        text_surf = text.render(f'Player 2 ({len(self.player2_cards)})', True, (0, 0, 0))
        game_display.blit(text_surf, (5, height - 20))

        status = "Battle"
        color = (0, 0, 0)
        if self.shuffling:
            status = "Shuffling"
        elif self.dealing:
            status = "Dealing"
        elif self.battle_winner:
            status = f"Player {self.battle_winner} wins"
        elif self.war:
            color = (255, 0, 0)
            status = "War!"
            
        text_surf = text.render(status, True, color)
        game_display.blit(text_surf, (5, (height / 2) - 20))
    def reset(self):
        pass


