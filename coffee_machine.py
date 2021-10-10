# define coffee class
import time


class CoffeeType:
    def __init__(self, name, water, milk, coffee, price):
        self.name = name
        self.water = water
        self.milk = milk
        self.coffee = coffee
        self.price = price

# create three instances of coffee


latte = CoffeeType(name="Latte", water=200, milk=150, coffee=24, price=2.5)
espresso = CoffeeType(name="Espresso", water=50, milk=0, coffee=18, price=1.5)
cappuccino = CoffeeType(name="Cappuccino", water=250, milk=50, coffee=24, price=3)

MENU = [latte, espresso, cappuccino]

# define the class Coffee_machine


class CoffeeMachine:
    def __init__(self):
        self.water = 2000
        self.milk = 2000
        self.money_in_box = 0
        self.coffee = 1000
        self.resources = {'Water': [self.water, 'mL'], 'Milk': [self.milk, 'mL'],
                          'Coffee': [self.coffee, 'g'], 'Money': [self.money_in_box, '€']}

    def report(self):
        """ Prints the report"""
        print('\n' + '*'*20)
        print('These are the available resources:')
        for item, quantity in self.resources.items():
            print(f'{item}: {quantity[0]} {quantity[1]}')
        print('*' * 20 + '\n')

    def check_resources(self, coffee_type):
        """
        Check if there are enough resources in machine to serve the selected drink
        returns enough boolean
        """

        coffee_requirements = [coffee_type.water, coffee_type.milk, coffee_type.coffee]

        for index, value in enumerate(self.resources.values()):
            if value[0] < coffee_requirements[index]:
                # not enough resources to serve the drink
                return False

            return True

    # def available_drinks(self, drinks: object = [latte, espresso, cappuccino]):
    def available_drinks(self):
        """
        Updates the list of available drinks
        returns list of available drinks
        """
        available_list =[]
        for drink in MENU:
            if self.check_resources(drink):
                available_list.append(drink)

        return available_list

    def ask_drink(self):
        """
        Asks for an option in main menu
        return selected_coffee if everything goes well
        """

        while True:
            # List of currently available drinks
            print(f"Available drinks: ")
            currently_available = self.available_drinks()
            # False if current_available is empty list
            if not currently_available:
                print('There are no available drinks. Coffee machine run out of resources.'
                      '\nSorry for the inconvenience.\n')
                self.report()
                return 'switch off'

            # print the available menu and their prices
            for drink in currently_available:
                print(f"{drink.name}, {drink.price} €")

            # list of names of drinks in menu
            drink_names = [i.name for i in MENU]
            # list of names of currently available drinks
            currently_available_names = [i.name for i in currently_available]

            # ask for choice
            choice = input("What would you like? ")
            # check if choice is a valid drink
            if choice.title() in currently_available_names:

                # check if choice is a valid drink
                for drink in MENU:
                    if choice.title() == drink.name:
                        selected_coffee = drink
                        print(f"Your choice is '{choice.title()}' and it costs "
                              f"{selected_coffee.price} €")
                        return selected_coffee

            # check if user choice is not currently available
            elif choice.title() in drink_names:

                print('Your choice is not available at this moment.\n'
                      'Please, choose other drink among our currently available options.')
                continue

            # check if user meant switch off machine or get a report
            elif choice in ['off', 'report']:

                if choice == 'off':
                    return 'switch off'
                elif choice == 'report':
                    self.report()
                    continue

            # Wrong input, ask again
            else:
                print("Please, enter a valid option.\n")

    def serve(self, coffee_type):
        """
        Subtracts ingredients from coffee machine
        :param coffee_type:
        :return: none
        """
        # subtract the following amounts from available resources
        self.water -= coffee_type.water
        self.milk -= coffee_type.milk
        self.coffee -= coffee_type.coffee
        print(f"Your {coffee_type.name.title()} is ready. Enjoy it!\n")
        self.resources = {'Water': [self.water, 'mL'],
                          'Milk': [self.milk, 'mL'],
                          'Coffee': [self.coffee, 'g'],
                          'Money': [self.money_in_box, '€']
                          }

    def count_coins(self):
        """
        asks for amount of every kind of coin
        :return: inserted_money
        """
        inserted_money = 0
        
        coins = {'5 cents': 0.05,
                 '10 cents': 0.1,
                 '50 cents': 0.5,
                 '1 euro': 1,
                 '2 euros': 2
                 }

        for coin_name, value in coins.items():
                  
            while True:
                num_coins = input(f'{coin_name} coins? ')
                # any inserted coin of that type
                if num_coins == '':
                    break
                else:
                    try:  # check if it was a number of coins
                        num_coins = int(num_coins)

                    except ValueError:
                        print(f'Please, enter a valid number of {coin_name} '
                              f'coins. Try again...')
                        continue
                    inserted_money += num_coins * value
                    break
        print(f"You inserted {inserted_money:.2f} euros")
        return inserted_money

    def check_enough_money(self, coffee_type, inserted_amount):
        """
        checks if the inserted money is enough to pay the drink
        asks for more money if not sufficient
        goes back to main menu if user does not want to enter more money to
        pay the selected drink
        :param coffee_type:
        :param inserted_amount:
        :return: 0 -> no change, -1 -> user did not want to pay enough for the drink
        """
        price = coffee_type.price
        # is enough to pay coffee
        if price <= inserted_amount:
            self.money_in_box += price  # add money to machine box
            if price < inserted_amount:
                return inserted_amount - price
            return 0  # no change to return
        # not enough money
        else:
            print("The inserted money was not enough to pay the selected drink.")
            print(f'You have to introduce {price - inserted_amount:.2f} euros more'
                  f' to get your drink, please.')
            # give second opportunity to add what is left
            while True:
                keep_on = input("Do you want to add more coins? [Y/N] ")
                if keep_on in ['Y', 'y', 'yes', 'YES']:
                    inserted_amount += self.count_coins()
                    self.check_enough_money(coffee_type, inserted_amount)
                else:
                    return -1


my_vending = CoffeeMachine()

while True:

    chosen_coffee = my_vending.ask_drink()
    # turn off machine
    if chosen_coffee == 'switch off':
        print('Turning off the coffee machine...')
        time.sleep(1)
        break

    else:
        # check if there are enough resources to serve the coffee
        if my_vending.check_resources(chosen_coffee):
            # ask for coins
            inserted_money = my_vending.count_coins()
            # check if price <= entered money
            change = my_vending.check_enough_money(chosen_coffee, inserted_money)
            if change != -1:
                my_vending.serve(chosen_coffee)
                if change != 0:
                    print(f"And don't forget your change! {change:.2f} €\n")
            else:
                chosen_coffee = my_vending.ask_drink()
