def blackjack():
    
    #Set up the chips outside the while-loop to gain more and more:
    player_chips = Chips(500)
    
    while True:
        
        # Print an opening statement
        print("Welcome to BlackJack!")
        print("Get as close to 21 as you can without going over!")
        print("The dealer hits until she reaches 17")
        print("Aces count as 11 or 1")
        print("By @sebhaugeto")
        
        #Ask if human wants to play
        while True:
            global answer
            answer = input("Would you like to start the game? (yes/no)")
            if answer in ("yes","no"):
                break
            else:
                print("Please answer yes or no")
                
        if answer == "no":
            clear_output()
            print("Fuck u too. Goodbye.") 
            break
            
        # Create & shuffle the deck, deal two cards to each player
        clear_output()
        deck = Deck()
        deck.shuffle()

        player = Hand()
        player.add_card(deck.deal())
        player.add_card(deck.deal())

        dealer = Hand()
        dealer.add_card(deck.deal())
        dealer.add_card(deck.deal())

        # Set up the Player's chips
        print("\nYou have " + str(player_chips.total) + " chips to play with")

        # Prompt the Player for their bet
        take_bet(player_chips)

        while True:  # from hit_or_stand function
            
            # Show cards (but keep one dealer card hidden)
            clear_output()
            show_some(player,dealer)
            
            # Prompt for Player to Hit or Stand
            while True:
                #check for instant blackjack:
                if player.value == 21:
                    print("INSTANT BLACKJACK! Dealer's turn.")
                    break
                    
                #ask player if he wants to hit or stand
                print("\n")
                hit_stand = input("Would you like to hit or stand? ")
                if hit_stand in ("hit","stand"):
                    break
                else:
                    print("Choose betwwen 'hit' or 'stand'")
                    continue 

            if hit_stand == "hit":
                hit(deck,player)

            else:
                clear_output()
                print("\n")
                print("Player stands. Dealer is playing")
                break
        
            show_some(player,dealer)
            
            #If blackjack:
            if player.value == 21:
                print("BLACKJACK! Dealer's turn.")
                break
            
            #if over 21
            if player.value > 21:
                player_busts(player_chips)
                break

        # If over 21:
        if player.value <= 21:
            show_all(player,dealer)
            while dealer.value < 17:
                dealer.add_card(deck.deal())
                print("\n")
                show_all(player,dealer)
                print("\n")
            
        # Run different winning scenarios
            print("\n")
            if player.value > dealer.value:
                player_wins(player_chips)

            if dealer.value > player.value and dealer.value <= 21:
                dealer_wins(player_chips)

            if dealer.value > 21:
                dealer_busts(player_chips)

            if dealer.value == player.value:
                push()
        

        # Inform Player of their chips total 
        print("\n")
        print("You now have " + str(player_chips.total) + " chips")
        
        # Ask to play again
        while True:
            answer = input("Play again? (yes/no)")
            if answer in ("yes","no"):
                break
            else:
                print("Please answer yes or no")

        if answer == "yes":
            clear_output()
            continue

        else:
            print("Goodbye. Game by @sebhaugeto")
            break
          
# Classes and Functions
import random

suits = ("Hearts","Diamonds","Spades","Clubs")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

def clear_output():
    for i in range(50):
        print()

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return (self.rank + " of " + self.suit)

class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n  "+card.__str__()
        return ("The deck consists of " + str(len(self.deck)) + (" cards:") + deck_comp)
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card
    
class Hand:
    
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        if card.rank == "Ace":
            self.aces += 1
            
    def adjust_for_ace(self):
        #default value of Ace is 11. Only need to adjust where we'd want 1
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
            
class Chips:
    
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
    

def take_bet(chips):
    #chips will be a Chips (the class), so it will have two attributes, self.total og self.bet
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("A bet must be an integer, idiot!")
            continue 
        else:
            if chips.total < chips.bet:
                print("Sorry, but your bet can't exceed " + str(chips.total))
            else:
                break
            
def hit(deck,hand):
    
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
 
# Functions to display cards
def show_some(player,dealer):
    print("\nDealer's Hand: | Value = " + str(values[dealer.cards[1].rank]))
    print("*card hidden*")
    print(dealer.cards[1])
    print("\nPlayer Hand: | Value = " + str(player.value))
    print(*player.cards, sep="\n")
    
    
def show_all(player,dealer):
    print("\nDealer Hand: | Value = " + str(dealer.value))
    print(*dealer.cards, sep="\n")
    print("\nPlayer Hand: | Value = " + str(player.value))
    print(*player.cards, sep="\n")
    
# Functions to handle game scenarios
def player_busts(chips):
    chips.lose_bet()
    print("PLAYER BUSTS! :(")
        
def player_wins(chips):
    chips.win_bet()
    print("PLAYER WINS! :D")

def dealer_busts(chips):
    chips.win_bet()
    print("DEALER BUSTS! :D")
    
def dealer_wins(chips):
    chips.lose_bet()
    print("DEALER WINS!  :*(")
    
def push():
    print("it's a push!")

blackjack()