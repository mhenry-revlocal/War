import pygame
from models.deck import Deck

class GameController(object):

    def __init__(self, game_display, display_width, display_height):
        self.game_display = game_display
        self.display_width = display_width
        self.display_height = display_height
        self.deck_pos =  (display_width - 150, (display_height / 2) - 43)
        self.background_image = pygame.transform.scale(pygame.image.load('images/card_background/background.jpg'), (display_width, display_height))
        self.cardback_image = pygame.transform.scale(pygame.image.load('images/Cards/cardBack_red2.png'), (70, 95))
        self.player1_deck_pos = (180, 30)
        self.player2_deck_pos = (180, display_height - 100)
        self.player1_battle_pos = (180, 140)
        self.player2_battle_pos = (180, display_height - 100 - 150)
        self.increase_speed = None
        self.quit = False
        self.paused = False
        self.speed = 1
        self.reset()
    
    def reset(self):
        self.deck = Deck()
        self.shuffling = False
        self.dealing = True
        self.shuffle_step = 1
        self.deal_step = 1
        self.dealing_card = None
        self.player1_cards = []
        self.player2_cards = []
        self.battle = False
        self.battle_step = 0
        self.player1_battle_cards = []
        self.player2_battle_cards = []
        self.display_battle = False
        self.battle_winner = None
        self.war = False
        self.war_step = 0
        self.war_again = False
        self.war_drawing = False
        self.player1_war_cards = []
        self.player2_war_cards = []
        self.player1_drawing_war_cards = []
        self.player2_drawing_war_cards = []
        self.collecting = False
        self.collecting_step = 0
        self.game_winner = None

    def act(self):
        self.handle_events() 
        if not self.paused:
            if self.dealing:
                self.dealing_act()
            elif self.battle:
                self.battle_act()
            elif self.war:
                self.war_act()
            elif self.collecting:
                self.collecting_act()
        
    def draw(self):
        self.game_display.blit(self.background_image, (0, 0))

        if self.shuffling:
            self.shuffling_draw()
        else:
            self.decks_draw()

        self.dealing_draw()
        self.drawing_draw()
        self.war_draw()
        self.battle_draw()
        self.collecting_draw()
        self.draw_labels()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.quit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.reset()
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_UP:
                    if self.increase_speed and self.increase_speed < 3:
                        self.increase_speed += 1
                    if not self.increase_speed and self.speed < 3:
                        self.increase_speed = self.speed + 1
                if event.key == pygame.K_DOWN:
                    if self.increase_speed and self.increase_speed > 1:
                        self.increase_speed -= 1
                    if not self.increase_speed and self.speed > 1:
                        self.increase_speed = self.speed - 1

    def check_speed_increase(self):
        if self.increase_speed:
            self.speed = self.increase_speed
            self.increase_speed = None

    def dealing_act(self):
        self.check_speed_increase()
        if self.speed == 3:
            if self.dealing_card:
                if len(self.player1_cards) <= len(self.player2_cards):
                    self.player1_cards.append(self.dealing_card)
                else:
                    self.player2_cards.append(self.dealing_card)
                self.dealing_card = None

            while len(self.deck.cards) > 0:
                if len(self.player1_cards) <= len(self.player2_cards):
                    self.player1_cards.append(self.deck.cards.pop())
                else:
                    self.player2_cards.append(self.deck.cards.pop())

            self.dealing = False
            self.battle = True
        else:
            deal_speed = 10
            if self.speed == 2:
                deal_speed = 1
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

    def battle_act(self):
        if self.battle_step == 0:
            if len(self.player1_cards) == 0:
                self.game_winner = 2
                self.battle = False
            elif len(self.player2_cards) == 0:
                self.game_winner = 1
                self.battle = False
            else:
                self.battle_step = 1
                self.player1_battle_cards.append(self.player1_cards.pop())
                self.player2_battle_cards.append(self.player2_cards.pop())
        else:
            self.battle_step += 1
            if ((self.speed == 1 and self.battle_step == 20) 
                or (self.speed == 2 and self.battle_step == 10)
                or (self.speed == 3 and self.battle_step == 2)):
                self.display_battle = True
                if self.player1_battle_cards[0].value > self.player2_battle_cards[0].value:
                    self.battle_winner = 1
                elif self.player1_battle_cards[0].value < self.player2_battle_cards[0].value:
                    self.battle_winner = 2
                else:
                    self.war = True
                    self.battle = False
                    self.battle_step = 0
            if ((self.speed == 1 and self.battle_step > 150) 
                or (self.speed == 2 and self.battle_step > 60)
                or (self.speed == 3 and self.battle_step > 2)):
                self.display_battle = False
                self.collecting_step = 0
                self.collecting = True
                self.battle = False
                self.war = False
                self.battle_step = 0
                self.check_speed_increase()

    def war_act(self):
        if self.war_step == 0:
            self.war_step = 1
            if len(self.player1_cards) < 4:
                self.game_winner = 2
                self.war = False
            elif len(self.player2_cards) < 4:
                self.game_winner = 1
                self.war = False
            else:
                for x in range(4):
                    self.player1_drawing_war_cards.append(self.player1_cards.pop())
                    self.player2_drawing_war_cards.append(self.player2_cards.pop())
        else:
            self.war_step += 1
            if ((self.speed == 1 and self.war_step == 20)
                or (self.speed == 2 and self.war_step == 10)
                or (self.speed == 3 and self.war_step == 2)):
                for x in range(3):
                    self.player1_war_cards.append(self.player1_drawing_war_cards.pop())
                    self.player2_war_cards.append(self.player2_drawing_war_cards.pop())
                self.player1_battle_cards.append(self.player1_drawing_war_cards.pop())
                self.player2_battle_cards.append(self.player2_drawing_war_cards.pop())

                if self.player1_battle_cards[-1].value > self.player2_battle_cards[-1].value:
                    self.battle_winner = 1
                elif self.player1_battle_cards[-1].value < self.player2_battle_cards[-1].value:
                    self.battle_winner = 2
                else:
                    self.war_again = True
            if ((self.speed == 1 and self.war_step > 300 and self.war_again)
                or (self.speed == 2 and self.war_step > 100 and self.war_again)
                or (self.speed == 3 and self.war_step > 2 and self.war_again)):
                self.war_step = 0
                self.war_again = False
            if ((self.speed == 1 and self.war_step > 150 and not self.war_again)
                or (self.speed == 2 and self.war_step > 70 and not self.war_again)
                or (self.speed == 3 and self.war_step > 2 and not self.war_again)):
                self.display_battle = False
                self.dislay_war = False
                self.collecting_step = 0
                self.collecting = True
                self.battle = False
                self.battle_step = 0
                self.war = False
                self.war_step = 0
                self.check_speed_increase()

    def collecting_act(self):
        if self.collecting_step == 0:
            self.collecting_step = 1
        elif ((self.speed == 1 and self.collecting_step < 40)
            or (self.speed == 2 and self.collecting_step < 15)
            or (self.speed == 3 and self.collecting_step < 2)):
            self.collecting_step += 1
        else:
            if self.battle_winner == 1:
                for x in range(len(self.player1_battle_cards)):
                    self.player1_cards.insert(0, self.player1_battle_cards.pop())
                    self.player1_cards.insert(0, self.player2_battle_cards.pop())
                for x in range(len(self.player1_war_cards)):
                    self.player1_cards.insert(0, self.player1_war_cards.pop())
                    self.player1_cards.insert(0, self.player2_war_cards.pop())
            if self.battle_winner == 2:
                for x in range(len(self.player1_battle_cards)):
                    self.player2_cards.insert(0, self.player1_battle_cards.pop())
                    self.player2_cards.insert(0, self.player2_battle_cards.pop())
                for x in range(len(self.player1_war_cards)):
                    self.player2_cards.insert(0, self.player1_war_cards.pop())
                    self.player2_cards.insert(0, self.player2_war_cards.pop())
            self.collecting = False
            self.war = False
            self.battle = True
            self.battle_winner = None
            self.check_speed_increase()

    def shuffling_draw(self):
        half_size = int(len(self.deck.cards) / 2)
        if self.shuffle_step < 130:
            cut_pos = (self.display_width - 150 - self.shuffle_step + half_size, (self.display_height / 2) - 43 - half_size)
        else:
            cut_pos = (self.display_width - 150 - 130 + half_size, (self.display_height / 2) - 43 - half_size + self.shuffle_step - 130)
        for i in range(half_size):
            self.game_display.blit(self.cardback_image, (self.deck_pos[0] + i, self.deck_pos[1] - i))
        for i in range(half_size):
            self.game_display.blit(self.cardback_image, (cut_pos[0] + i, cut_pos[1] - i))
        self.shuffle_step += 2

    def decks_draw(self):
        for i in range(len(self.deck.cards)):
            self.game_display.blit(self.cardback_image, (self.deck_pos[0] + i, self.deck_pos[1] - i))
        for i in range(len(self.player1_cards)):
            self.game_display.blit(self.cardback_image, (self.player1_deck_pos[0] + i, self.player1_deck_pos[1] - i))
        for i in range(len(self.player2_cards)):
            self.game_display.blit(self.cardback_image, (self.player2_deck_pos[0] + i, self.player2_deck_pos[1] - i))

    def dealing_draw(self):
        if self.dealing_card:
            increment = self.deal_step * 14
            if self.speed == 2:
                increment = self.deal_step * 50
            if self.deal_step > 0:
                self.game_display.blit(self.cardback_image, (self.deck_pos[0] - increment, self.deck_pos[1] - increment))
            elif self.deal_step < 0:
                self.game_display.blit(self.cardback_image, (self.deck_pos[0] + increment, self.deck_pos[1] - increment))
    
    def battle_draw(self):
        if self.display_battle:
            self.game_display.blit(self.player1_battle_cards[-1].image, self.player1_battle_pos)       
            self.game_display.blit(self.player2_battle_cards[-1].image, self.player2_battle_pos)       
    
    def drawing_draw(self):
        if self.battle and not self.display_battle:
            increment = self.battle_step * 6
            self.game_display.blit(self.cardback_image, (self.player1_deck_pos[0], self.player1_deck_pos[1] + increment))
            self.game_display.blit(self.cardback_image, (self.player2_deck_pos[0], self.player2_deck_pos[1] - increment))

        if len(self.player1_drawing_war_cards) > 0:
            increment = self.war_step * 6
            self.game_display.blit(self.cardback_image, (self.player1_deck_pos[0], self.player1_deck_pos[1] + increment))
            self.game_display.blit(self.cardback_image, (self.player1_deck_pos[0] + increment, self.player1_deck_pos[1] + increment))
            self.game_display.blit(self.cardback_image, (self.player1_deck_pos[0] + increment, self.player1_deck_pos[1] + increment))
            self.game_display.blit(self.cardback_image, (self.player1_deck_pos[0] + increment, self.player1_deck_pos[1] + increment))
            self.game_display.blit(self.cardback_image, (self.player2_deck_pos[0], self.player2_deck_pos[1] - increment))
            self.game_display.blit(self.cardback_image, (self.player2_deck_pos[0] + increment, self.player2_deck_pos[1] - increment))
            self.game_display.blit(self.cardback_image, (self.player2_deck_pos[0] + increment, self.player2_deck_pos[1] - increment))
            self.game_display.blit(self.cardback_image, (self.player2_deck_pos[0] + increment, self.player2_deck_pos[1] - increment))

    def war_draw(self):
        if len(self.player1_war_cards) > 0 and not self.collecting:
            for i in range(int(len(self.player1_war_cards) / 3)):
                self.game_display.blit(self.cardback_image, (self.player1_battle_pos[0] + 75 + i, self.player1_battle_pos[1] - i))
                self.game_display.blit(self.cardback_image, (self.player1_battle_pos[0] + 150 + i, self.player1_battle_pos[1] - i))
                self.game_display.blit(self.cardback_image, (self.player1_battle_pos[0] + 225 + i, self.player1_battle_pos[1] - i))
                self.game_display.blit(self.cardback_image, (self.player2_battle_pos[0] + 75 + i, self.player2_battle_pos[1] - i))
                self.game_display.blit(self.cardback_image, (self.player2_battle_pos[0] + 150 + i, self.player2_battle_pos[1] - i))
                self.game_display.blit(self.cardback_image, (self.player2_battle_pos[0] + 225 + i, self.player2_battle_pos[1] - i))

    def collecting_draw(self):
        if self.collecting and len(self.player1_battle_cards) > 0:
            increment = -(self.collecting_step * 9)
            if self.battle_winner == 2:
                increment = -(increment)

            if self.speed == 2:
                increment *= 3

            self.game_display.blit(self.player1_battle_cards[-1].image, (self.player1_battle_pos[0], self.player1_battle_pos[1] + increment))      
            self.game_display.blit(self.player2_battle_cards[-1].image, (self.player2_battle_pos[0], self.player2_battle_pos[1] + increment))      

            if len(self.player1_war_cards) > 0:
                self.game_display.blit(self.cardback_image, (self.player1_battle_pos[0] + 75, self.player1_battle_pos[1] + increment))
                self.game_display.blit(self.cardback_image, (self.player1_battle_pos[0] + 150, self.player1_battle_pos[1] + increment))
                self.game_display.blit(self.cardback_image, (self.player1_battle_pos[0] + 225, self.player1_battle_pos[1] + increment))
                self.game_display.blit(self.cardback_image, (self.player2_battle_pos[0] + 75, self.player2_battle_pos[1] + increment))
                self.game_display.blit(self.cardback_image, (self.player2_battle_pos[0] + 150, self.player2_battle_pos[1] + increment))
                self.game_display.blit(self.cardback_image, (self.player2_battle_pos[0] + 225, self.player2_battle_pos[1] + increment))

    def draw_labels(self):
        text = pygame.font.Font('freesansbold.ttf', 20)
        text_sm = pygame.font.Font('freesansbold.ttf', 12)

        text_surf = text.render(f'Player 1 ({len(self.player1_cards)})', True, (0, 0, 0))
        self.game_display.blit(text_surf, (5, 5))

        pausetxt = 'p = pause'
        if self.paused:
            pausetxt = 'p = unpause'
        text_surf = text_sm.render(pausetxt, True, (0, 0, 0))
        self.game_display.blit(text_surf, (5, 50))

        text_surf = text_sm.render('r = reset', True, (0, 0, 0))
        self.game_display.blit(text_surf, (5, 70))

        text_surf = text_sm.render('esc/q = quit', True, (0, 0, 0))
        self.game_display.blit(text_surf, (5, 90))

        if (self.increase_speed and self.increase_speed < 3) or (not self.increase_speed and self.speed < 3):
            text_surf = text_sm.render('up = increase speed', True, (0, 0, 0))
            self.game_display.blit(text_surf, (5, 110))

        if (self.increase_speed and self.increase_speed > 1) or (not self.increase_speed and self.speed > 1):
            y = 130
            if self.speed == 3:
                y = 110
            text_surf = text_sm.render('down = decrease speed', True, (0, 0, 0))
            self.game_display.blit(text_surf, (5, y))

        text_surf = text.render(f'Player 2 ({len(self.player2_cards)})', True, (0, 0, 0))
        self.game_display.blit(text_surf, (5, self.display_height - 20))

        status = "Battle"
        color = (0, 0, 0)
        if self.paused:
            status = "Paused"
        elif self.shuffling:
            status = "Shuffling"
        elif self.dealing:
            status = "Dealing"
        elif self.battle_winner:
            status = f"Player {self.battle_winner} wins"
        elif self.game_winner:
            color = (0, 255, 0)
            status = f"Player {self.game_winner} wins"
        elif self.war:
            color = (255, 0, 0)
            status = "War!"
            
        text_surf = text.render(status, True, color)
        self.game_display.blit(text_surf, (5, (self.display_height / 2) - 20))