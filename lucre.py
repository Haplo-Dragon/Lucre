#!/usr/bin/python

import sys
import re

COINS = ['Gold', 'Silver', 'Copper']
wealth = {}
exchange = {'Gold': 1, 'Silver': 10, 'Copper': 100}

for item in COINS:
    wealth[item] = int(input("How much %s do you have?\n" % item))

for coin_type in sorted(wealth.keys()):
    if coin_type is not 'Gold':
        exchange[coin_type] = int(input("How many %s pieces in 1 gold piece?\n" % coin_type))


def transact(starting_wealth, amount, exchange_rate, transaction_type):
    # Form a list of tuples by pairing coin types and regex letters one to one - ('Gold', '[g]'), ('Silver', '[s]') etc.
    denominations = zip(COINS, ['g', 's', 'c'])
    denom = list(denominations)
    p = re.compile(r"""
                           ([0-9]+)        # Any number of digits; the parentheses mean we are capturing this bit
                                           # for later use.
                           [gsc]              # Followed by the current denomination (g, s, or c)
                           """,
                   re.VERBOSE)
    iterator = p.finditer(amount)

    for match in iterator:
        currency = None
        for item in denom:
            if match.group()[-1] == item[1]:
                currency = item[0]

        change = int(match.group(1))

        if transaction_type == 'SPEND':
            change = -change

        if starting_wealth[currency] + change < 0:
            if currency == 'Gold':
                print("You can't afford it!\n")
                input("Press any key to feel poor.\n")
            else:
                tier_above = COINS.index(currency) - 1

                orig_wealth = {}
                for key, value in starting_wealth.items():
                    orig_wealth[key] = value

                while abs(change) > starting_wealth[currency]:
                    if tier_above < 0:
                        print("You can't afford it!")
                        input("Press any key to feel poor.\n")
                        starting_wealth = orig_wealth
                        return starting_wealth
                    if starting_wealth[COINS[tier_above]] > 0:
                        starting_wealth[COINS[tier_above]] -= 1
                        starting_wealth[currency] += int(exchange_rate[currency] / exchange_rate[COINS[tier_above]])
                    else:
                        tier_above -= 1

                starting_wealth[currency] += change
        else:
            starting_wealth[currency] += change

    return starting_wealth


if __name__ == "__main__":
    choice = None
    menu = {
        '1.': 'Spend money',
        '2.': 'Earn money',
        '3.': 'Exit'
    }
    while True:
        options = sorted(menu.keys())
        print("\nYou have:\n\t %s GP\n\t %s SP\n\t %s CP\n" % (wealth['Gold'], wealth['Silver'], wealth['Copper']))
        for entry in options:
            print(entry, menu[entry])
        try:
            choice = int(input("\nChoice: "))
        except ValueError:
            print("That wasn't one of the choices. Carbon-based lifeforms are so fallible.")
            choice = None

        if choice == 1:
            price = input("How much did you squander THIS time? (In the format '4g 10s 56c')\n")
            wealth = transact(wealth, price, exchange, transaction_type='SPEND')
        if choice == 2:
            new_money = input("How much filthy lucre? (In the format '4g 10s 56c')\n")
            wealth = transact(wealth, new_money, exchange, transaction_type='EARN')
        if choice == 3:
            sys.exit()
