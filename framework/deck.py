from framework.card import Suits, Cards, Card
import random

class Deck(object):
    def __init__(self):
        self.cards = []
        self.reset()
        pass
    def reset(self):
        self.cards = []
        for suit in Suits:
            for card in Cards:
                self.cards.append(Card(suit, card))
        random.shuffle(self.cards)


