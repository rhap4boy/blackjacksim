import numpy as np
from colorama import Fore, Back, Style
from multiprocessing import shared_memory

value = {'A': 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 'J': 10, 'Q': 10, 'K': 10}
player_title = "Player's Total          "


# Stats Model
class StatsModel(object):
    def __init__(self):
        return

    def initialize(self):
        ss = shared_memory.SharedMemory(name="stay_stats", create=True, size=1936)
        hs = shared_memory.SharedMemory(name="hit_stats", create=True, size=1936)

        self.stay_stats = np.ndarray((22, 11), dtype="float64", buffer=ss.buf)
        self.hit_stats = np.ndarray((22, 11), dtype="float64", buffer=hs.buf)

        # Initialize Arrays to Zero
        for i in range(1, 22):
            for j in range(1, 11):
                self.stay_stats[i][j] = 0
                self.hit_stats[i][j] = 0

        for i in range(0, 11):
            self.hit_stats[0][i] = i
            self.stay_stats[0][i] = i

        for i in range(0, 22):
            self.hit_stats[i][0] = i
            self.stay_stats[i][0] = i

    def get_hit_stats(self):
        hs = shared_memory.SharedMemory(name='hit_stats')
        c = np.ndarray((22, 11), dtype="float64", buffer=hs.buf)
        return np.copy(c)

    def get_stay_stats(self):
        ss = shared_memory.SharedMemory(name='stay_stats')
        c = np.ndarray((22, 11), dtype="float64", buffer=ss.buf)
        return np.copy(c)

    def lookup(self, card):
        return value[card]

    def add_hit_stats(self, stats1, stats2):
        # print("add ", stats1, stats2)
        hs = shared_memory.SharedMemory(name='hit_stats')
        c = np.ndarray((22, 11), dtype="float64", buffer=hs.buf)
        c[stats1][self.lookup(stats2)] = c[stats1][self.lookup(stats2)] + 1

    def add_stay_stats(self, stats1, stats2):
        # print("add ", stats1, stats2)
        ss = shared_memory.SharedMemory(name='stay_stats')
        c = np.ndarray((22, 11), dtype="float64", buffer=ss.buf)
        c[stats1][self.lookup(stats2)] = c[stats1][self.lookup(stats2)] + 1

    def update(self, value1, value2, value3):
        if value3:
            self.add_hit_stats(value1, value2)
        else:
            self.add_stay_stats(value1, value2)
        return

    def reset(self):
        ss = shared_memory.SharedMemory(name="stay_stats")
        hs = shared_memory.SharedMemory(name="hit_stats")

        self.stay_stats = np.ndarray((22, 11), dtype="float64", buffer=ss.buf)
        self.hit_stats = np.ndarray((22, 11), dtype="float64", buffer=hs.buf)

        for i in range(1, 22):
            for j in range(1, 11):
                self.stay_stats[i][j] = 0
                self.hit_stats[i][j] = 0


# Stats View
class StatsView(object):
    def __init__(self):
        return

    def print_hit_stats(self, stats):
        np.set_printoptions(suppress=True)
        print(stats)

    def print_stay_stats(self, stats):
        np.set_printoptions(suppress=True)
        print(stats)

    def print_strategy(self, stats1, stats2):
        sum = 0
        for i in range(1, 22):
            print(Fore.LIGHTYELLOW_EX + player_title[i - 2].ljust(2), end="")
            print(Fore.LIGHTWHITE_EX + str(i).rjust(2), end="")
            for j in range(1, 11):
                sum = sum + stats1[i][j] + stats2[i][j]
                if stats1[i][j] > stats2[i][j]:
                    print(Fore.GREEN + ' S', end="")
                else:
                    if stats1[i][j] == stats2[i][j]:
                        print(Fore.BLUE + ' .', end="")
                    else:
                        print(Fore.RED + ' H', end="")
            print("")
        print(Style.RESET_ALL)


# Stats Controller
class StatsController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def print_stats(self):
        print("Hit Stats")
        self.view.print_hit_stats(self.model.get_hit_stats())
        print("Stay Stats")
        self.view.print_stay_stats(self.model.get_stay_stats())

    def print_strategy(self):
        print(Fore.LIGHTYELLOW_EX + "       Dealer's Up Card")
        print(Fore.LIGHTWHITE_EX + "   0 A 2 3 4 5 6 7 8 910")
        self.view.print_strategy(self.model.get_stay_stats(), self.model.get_hit_stats())

    def add_hit_stats(self, value1, value2):
        return

    def add_stay_stats(self, value1, value2):
        return

    def update(self, value1, value2, value3):
        self.model.update(value1, value2, value3)

    def initialize(self):
        self.model.initialize()

    def reset(self):
        self.model.reset()
