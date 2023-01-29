import random

from Card import *

class Deck():
    """Object Manager for oCard."""
    SUIT_TUPLE = ('Diamonds', 'Clubs', 'Hearts', 'Spades')
    STANDART_DICT = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                        '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                        'Jack': 11, 'Queen': 12, 'King': 13}
    
    def __init__(self, window, rankValueDict=STANDART_DICT):
        """Initialize states and shuffle deck."""
        # rankValueDict defaults to STANDARD_DICT, but you can call 
        # with a different dict, e.g., a special dict for Blackjack
        self.startingDeckList = []
        self.playingDeckList = []
        for suit in Deck.SUIT_TUPLE:
            for rank, value in Deck.STANDART_DICT.items():
                oCard = Card(window, rank, suit, value)
                self.startingDeckList.append(oCard)
        
        self.shuffle()
    
    def shuffle(self):
        """Copy the starting deck and save it in the playing deck list"""
        self.playingDeckList = self.startingDeckList.copy()
        for oCard in self.playingDeckList:
            oCard.conceal()
        random.shuffle(self.playingDeckList)
    
    def getCard(self):
        """Pop one card off the deck and return it"""
        if len(self.playingDeckList) == 0:
            raise IndexError('No more cards, wiuuuwuuu')
        
        oCard = self.playingDeckList.pop()
        return oCard
    
    def returnCardToDeck(self, oCard):
        """Put card back into deck."""
        self.playingDeckList.insert(0, oCard)

# Test Deck
if __name__ == "__main__":

    import pygame

    WINDOW_WIDTH = 100
    WINDOW_HEIGHT = 100

    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    oDeck = Deck(window)
    for i in range(1, 53):
        oCard = oDeck.getCard()
        print('Name: ', oCard.getName, 'Value: ', oCard.getValue())