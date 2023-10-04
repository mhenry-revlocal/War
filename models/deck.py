from models.cards import Cards 
from models.suits import Suits
from models.card import Card
import random

class Deck(object):

    def __init__(self):
        self.cards = []
        self.reset()

    def reset(self):
        self.cards = []
        for suit in Suits:
            for card in Cards:
                self.cards.append(Card(suit, card))
        random.shuffle(self.cards)


