import pygwidgets
from Constants import *
from Deck import *
from Card import *

class Game():
    # Card placement on the board
    CARD_OFFSET = 110 # Buffer amount between cards on the board
    CARDS_TOP = 300 # Cards placed on the y-axis
    CARDS_LEFT = 75 # As in cards left to each other; x-axis

    NCARDS = 8 # Number of cards allowed on the board
    POINTS_CORRECT = 15
    POINTS_INCORRECT = 10

    def __init__(self, window):
        self.window = window
        self.oDeck = Deck(self.window) # Instanciate Deck
        self.score = 100 # Score
        # Text
        self.scoreText = pygwidgets.DisplayText(window, (450, 164),
                                    'Score: ' + str(self.score),
                                    fontSize=36, textColor=WHITE,
                                    justified='right')

        self.messageText = pygwidgets.DisplayText(window, (50, 460),
                                    '', width=900, justified='center',
                                    fontSize=27, textColor=WHITE)
        # Sounds
        self.loserSound = pygame.mixer.Sound("sounds/sounds_loser.wav")
        self.winnerSound = pygame.mixer.Sound("sounds/sounds_ding.wav")
        self.cardShuffleSound = pygame.mixer.Sound("sounds/sounds_cardShuffle.wav")

        self.cardXPositionsList = [] # Stores the x position of the cards
        thisLeft = Game.CARDS_LEFT # Current cordinate of 1st card
         # Calculate the x positions of all cards, once
        for cardNum in range(Game.NCARDS):
            self.cardXPositionsList.append(thisLeft)
            thisLeft += Game.CARD_OFFSET

        self.reset() # Start new round of game

    def reset(self):
        """This method is called when a new round starts.
        ---Resets game.
        """
        self.cardShuffleSound.play()
        self.cardList = []
        self.oDeck.shuffle()
        for cardIndex in range(0, Game.NCARDS):
            oCard = self.oDeck.getCard()
            self.cardList.append(oCard)
            thisXPosition = self.cardXPositionsList[cardIndex]
            oCard.setLoc((thisXPosition, Game.CARDS_TOP))
        
        self.showCard(0) # Pass in the index of the card you wish to reveal.
        self.cardNumber = 0 # Index number for getCardNameAndValue method
        self.currentCardName, self.currentCardValue = \
                                        self.getCardNameAndValue(self.cardNumber)
        
        self.messageText.setValue(f'Starting card is {self.currentCardName} \
                                                will the next card be higher or lower?')
        
    def getCardNameAndValue(self, index):
        """Pass in the index of the card  
        ---to return both its name and value
        """
        oCard = self.cardList[index]
        theName = oCard.getName()
        theValue = oCard.getValue()
        return theName, theValue
    
    def showCard(self, index):
        """Pass in the index of the card you wish to reveal."""
        oCard = self.cardList[index]
        oCard.reveal()
    
    def hitHigherOrLower(self, higherOrLower):
        self.cardNumber += 1 # To be able to see the next card after choosing if its hogh or low
        self.showCard(self.cardNumber)
        nextCardName, nextCardValue = self.getCardNameAndValue(self.cardNumber)\
        
        if higherOrLower == HIGHER:
            if nextCardValue > self.currentCardValue:
                self.score += Game.POINTS_CORRECT
                self.messageText.setValue(f'Yes, the {nextCardName} was higher')
                self.winnerSound.play()
            else:
                self.score -= Game.POINTS_INCORRECT
                self.messageText.setValue(f'No, the {nextCardName} was not higher')
                self.loserSound.play()

        else: # User hit the lower button
            if nextCardValue < self.currentCardValue:
                self.score += Game.POINTS_CORRECT
                self.messageText.setValue(f'Yes, the {nextCardName} was lower')
                self.winnerSound.play()
            
            else:
                self.score -= Game.POINTS_INCORRECT
                self.messageText.setValue(f'No, the {nextCardName} was not lower')
                self.loserSound.play()
        
        self.scoreText.setValue(f'Score: {self.score}')

        self.currentCardValue = nextCardValue # Set up for the next card

        done = (self.cardNumber == (Game.NCARDS - 1)) # Did we reach the last card?
        return done

    def draw(self):
        """Tell each card to draw itself."""
        for oCard in self.cardList:
            oCard.draw()
        
        self.scoreText.draw()
        self.messageText.draw()