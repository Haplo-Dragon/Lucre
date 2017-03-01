#!/usr/bin/python

import sys
import re

COINS = ['Gold', 'Silver', 'Copper']
wealth = {}
exchange = {'Gold': 1, 'Silver': 10, 'Copper': 100}

for item in COINS:
    wealth[item] = int(input("How much %s do you have?\n" % item))

for coin_type in wealth:
    if coin_type is not 'Gold':
        exchange[coin_type] = int(input("How many %s pieces in 1 gold piece?\n" % coin_type))


def transact(starting_wealth, amount, exchange_rate, type):
    # Form a list of tuples by pairing coin types and regex letters one to one - ('Gold', '[g]'), ('Silver', '[s]') etc.
    denominations = zip(COINS, ['[g]', '[s]', '[c]'])
    for denom in denominations:
        p = re.compile(r"""
                        ([0-9]+)        # Any number of digits; the parentheses mean we are capturing this bit
                                        # for later use.
                        %s              # Followed by the current denomination (g, s, or c) from the loop
                        \b              # and ending with a word boundary.
                        """
                       % denom[1],  # Here's where we insert the current denomination from the loop
                       re.VERBOSE)

        match = p.findall(amount)
        if match:
            change = int(match[0])

            if type == 'SPEND':
                change = -change

            if starting_wealth[denom[0]] + change < 0:
                if denom[0] == 'Gold':
                    print("You can't afford it!")
                else:
                    tier_above = COINS.index(denom[0]) - 1
                    orig_wealth = {}

                    for key, value in starting_wealth.items():
                        orig_wealth[key] = value

                    while abs(change) > starting_wealth[denom[0]]:
                        if tier_above < 0:
                            print("You can't afford it!")
                            print("Setting starting wealth to: ", orig_wealth)
                            starting_wealth = orig_wealth
                            return starting_wealth
                        if starting_wealth[COINS[tier_above]] > 0:
                            starting_wealth[COINS[tier_above]] -= 1
                            starting_wealth[denom[0]] += int(exchange_rate[denom[0]] / exchange_rate[COINS[tier_above]])
                        else:
                            tier_above -= 1

                    starting_wealth[denom[0]] += change
            else:
                starting_wealth[denom[0]] += change

    return starting_wealth


def convert(denom, starting_wealth, change, exchange_rate):
    while change > starting_wealth[denom[0]]:
        pass


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
            price = input("How much did you squander this time? (In the format '4g 10s 56c')\n")
            wealth = transact(wealth, price, exchange, type='SPEND')
        if choice == 2:
            new_money = input("How much filthy lucre? (In the format '4g 10s 56c')\n")
            wealth = transact(wealth, new_money, exchange, type='EARN')
        if choice == 3:
            sys.exit()
