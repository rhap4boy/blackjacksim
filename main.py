# Main for BlackJack Basic Strategy Table Generator

import random
import asyncio
from timeit import default_timer as timer
from multiprocessing import Process, Value
from cardMVC import CardController
from cardMVC import CardModel
from cardMVC import CardView
from statsMVC import StatsController
from statsMVC import StatsModel
from statsMVC import StatsView
import os

n_inner_tasks = 10
n_outer_tasks = 10
global show_rounds
show_rounds = False


# Async Task Coroutine
async def task_coro(pid):
    strategy = StatsController(StatsModel(), StatsView())
    deck = CardController(CardModel("Deck"), CardView())
    player_hand = CardController(CardModel("Player"), CardView())
    dealer_hand = CardController(CardModel("Dealer"), CardView())
    # Shuffle Deck
    deck.new()
    deck.shuffle()
    # deck.show()

    # Deal Dealer's Card
    dealer_hand.deal(deck)
    if show_rounds:
        dealer_hand.show()

    # Deal Player's Card
    player_hand.deal(deck)
    if show_rounds:
        player_hand.show()

    # Randomly choose whether to hit or stay
    r = random.choice([True, False])
    t = player_hand.total()
    if r:
        if show_rounds:
            print("Player Hit")
        player_hand.hit(deck)
        if show_rounds:
            player_hand.show()
        if player_hand.total() > 21:
            if show_rounds:
                print("Player Bust!")
    else:
        if show_rounds:
            print("Player Stays")
        # playerHand.show()

    while dealer_hand.total() < 17:
        if show_rounds:
            print("Dealer Hit")
        dealer_hand.hit(deck)
        if show_rounds:
            dealer_hand.show()
        if dealer_hand.total() > 21:
            if show_rounds:
                print("Dealer Bust!")

    player_win, dealer_win = player_hand.wins(dealer_hand)
    if player_win:
        strategy.update(t, dealer_hand.get_card(1), r)
        # strategy.print_stats()
    # await asyncio.sleep(random.randint(0, 2) * 0.001)
    print( 'process:', os.getpid(), 'task:', pid,)


# Async Core
async def core2(n):
    tasks = [task_coro(i) for i in range(1, n)]
    await asyncio.gather(*tasks)


# Regular Core
def core(n):
    asyncio.run(core2(n))


# Main routine 2
def main2():
    for x in range(100):
        core()


# Main routine
def main():
    # counter = Value('i', 0)
    processes = [Process(target=core, args=(n_inner_tasks,)) for _ in range(n_outer_tasks)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()


def menu():
    global n_inner_tasks, n_outer_tasks, show_rounds
    selection = 0
    while selection != '7':
        print("--- Blackjack Basic Strategy Table Generator ---")
        print("")
        print("    # of tasks for each process needs to be large")
        print("    in order to see benefits of multiple processors")
        print("")
        print("1 - # of tasks for each process -", n_inner_tasks)
        print("2 - # of processes -", n_outer_tasks)
        print("3 - Show each round -", show_rounds)
        print("4 - Show current Stats & Strategy table")
        print("5 - Run")
        print("6 - Reset Strategy Table")
        print("7 - Quit")
        selection = input('Selection:')
        if selection == '1':
            n_inner_tasks = int(input('Inner Loop # of tasks:'))
        if selection == '2':
            n_outer_tasks = int(input('Outer Loop # of processes:'))
        if selection == '3':
            if not show_rounds:
                show_rounds = True
            else:
                show_rounds = False
        if selection == '4':
            # strategy.print_stats()
            strategy.print_strategy()
        if selection == '5':
            start = timer()
            main()
            end = timer()
            print(f'sequentially: {end - start}')
            print("")
        if selection == '6':
            strategy.reset()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Setup stats
    strategy = StatsController(StatsModel(), StatsView())
    strategy.initialize()
    # strategy.print_stats()
    # Start the timer
    # start = timer()

    # Call the main routine
    menu()
    # main()
    # main2()
    # End the timer - Print
    # end = timer()
    # print(f'sequentially: {end - start}')
    # strategy.print_stats()
    # strategy.print_strategy()
