import random
import numpy as np
from colorama import Fore, Back, Style

value = {'A': 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'J': 10, 'Q': 10, 'K': 10}


class CardModel(object):

    def __init__(self, name):
        self.cards = []
        self.name = name

    def new(self):
        self.cards = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4

    def add(self, card):
        self.cards.append(card)

    def get(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def pop(self):
        return random.choice(["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4)
        # return (self.cards.pop())

    def random(self):
        return random.choice(["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"] * 4)

    def lookup(self, card):
        return value[card]

    def total(self):
        sum1 = 0
        ace = False
        for i in self.cards:
            # print(i)
            if i == 'A':
                ace = True
            # sum = sum + self.lookup(i)
            sum1 = sum1 + value[i]
        if ace:
            if (sum1 + 10) <= 21:
                sum1 = sum1 + 10
        return sum1

    def clear(self):
        self.cards = []

    def bust(self):
        if self.total() > 21:
            return True
        else:
            return False

    def get_card(self, value1):
        return self.cards[value1]


class CardView(object):
    def __init__(self):
        return

    def print_cards(self, cards, name, total):
        print(name, cards, "=", total)

    def print_total(self, value):
        print(value)

    def print_header(self):
        print(Fore.LIGHTWHITE_EX + " 0 1 2 3 4 5 6 7 8 910")


class CardController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show(self):
        self.view.print_cards(self.model.get(), self.model.name, self.model.total())

    def deal(self, deck):
        # self.model.add(deck.pop())
        # self.model.add(deck.pop())
        self.model.add(self.model.random())
        self.model.add(self.model.random())

    def hit(self, deck):
        self.model.add(deck.pop())

    def new(self):
        self.model.new()

    def pop(self):
        return self.model.pop()

    def shuffle(self):
        self.model.shuffle()

    def show_total(self):
        self.view.print_total(self.model.total())

    def total(self):
        return self.model.total()

    def clear(self):
        self.model.clear()

    def bust(self):
        return self.model.bust()

    def get_card(self, number):
        return self.model.get_card(number)

    def wins(self, cards):
        player_wins = False
        dealer_wins = False
        if self.bust():
            # print("Player Bust!")
            dealer_wins = True
        else:
            if cards.bust():
                # print("Dealer Bust!")
                player_wins = True
            else:
                if self.total() > cards.model.total():
                    # print("Player Wins")
                    player_wins = True
                else:
                    if self.total() == cards.model.total():
                        player_wins = False
                        dealer_wins = False
                        # print("Ties")
                    else:
                        if self.total() < cards.model.total():
                            # print("Dealer Wins")
                            dealer_wins = True
        return player_wins, dealer_wins
