import pygame
from models.cards import Cards

class Card(object):
    def __init__(self, suit, card):
        self.suit = suit
        self.card = card

        if card == Cards.Jack:
            self.value = 11
        elif card == Cards.Queen:
            self.value = 12
        elif card == Cards.King:
            self.value = 13
        elif card == Cards.Ace:
            self.value = 14
        else:
            self.value = int(card.value)
        
        self.image = pygame.transform.scale(pygame.image.load(f'images/Cards/card{self.suit.value}{self.card.value}.png'), (70, 95))