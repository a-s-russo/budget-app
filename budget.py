class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.spend_pc = 0

    def get_balance(self):
        balance = 0
        for transaction in self.ledger:
            balance += transaction['amount']
        return balance

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.update_spend_pc()

    def withdraw(self, amount, description=""):
        if amount <= self.get_balance():
            self.ledger.append({"amount": -amount, "description": description})
            self.update_spend_pc()
            return True
        return False

    def transfer(self, amount, budget):
        if amount <= self.get_balance():
            withdraw_description = "Transfer to " + budget.category
            self.withdraw(amount, description=withdraw_description)
            deposit_description = "Transfer from " + self.category
            budget.deposit(amount, description=deposit_description)
            return True
        return False

    def print(self):
        print(self.category.center(30, '*')[0:30])
        for transaction in self.ledger:
            description = transaction['description'].ljust(23)[0:23]
            amount = "{:7.2f}".format(transaction['amount'])[0:7]
            print(description + amount)
        print('Total: ' + "{:.2f}".format(self.get_balance())[0:23])

    def update_spend_pc(self):
        expenditure = 0
        for transaction in self.ledger:
            if transaction['amount'] < 0:
                expenditure += transaction['amount']
        numerator = -expenditure
        denominator = self.get_balance() - expenditure
        if denominator != 0:
            expenditure_percentage = numerator / denominator * 100
        else:
            expenditure_percentage = 0
        self.spend_pc = expenditure_percentage


def round_down(num, divisor):
    return num - (num % divisor)


def create_spend_chart(*args):
    args = [arg for arg in args]
    args.sort(key=lambda cat: cat.spend_pc, reverse=True)
    plot_strings = []
    for category in args:
        expenditure_percentage = category.spend_pc
        circles_to_plot = int(round_down(expenditure_percentage, 10) / 10) + 1
        spaces_to_plot = 11 - circles_to_plot
        string_to_plot = ' ' * spaces_to_plot + 'o' * circles_to_plot
        plot_strings.append(string_to_plot)
        plot_strings.append(' ' * 11)
        plot_strings.append(' ' * 11)
    axis_strings = ['1' + ' ' * 10, '0987654321 ', '0' * 11, '|' * 11, ' ' * 11]
    graph_strings = axis_strings + plot_strings
    print('Percentage spent by category')
    for i in range(11):
        for s in graph_strings:
            print(s[i], end='')
        print('')

    print('    -' + '--' * (len(args) + 1))

    categories = [category.category for category in args]
    max_str_length = max([len(category) for category in categories])
    category_strings = []
    for category in categories:
        category_strings = category_strings + [category.ljust(max_str_length, ' '), ' ' * max_str_length,
                                               ' ' * max_str_length]
    filler = [' ' * max_str_length]
    category_strings = filler + filler + filler + filler + filler + category_strings
    for i in range(max_str_length):
        for category in category_strings:
            print(category[i], end='')
        print('')


clothing = Category('Clothing')
fun = Category('Fun')
fun.deposit(100, 'salary')
fun.withdraw(100, 'movies')
food = Category('Food')
auto = Category('Auto')
auto.deposit(1000, 'salary')
auto.withdraw(600, 'repair')
auto.transfer(200, food)
food.deposit(600.00, 'salary')
food.transfer(500, clothing)
clothing.withdraw(20, 't-shirt')
clothing.withdraw(230, 'handbag')
food.withdraw(5, 'milk and lots of other stuff that I bought')
food.withdraw(3, 'bread')
create_spend_chart(auto, clothing, food, fun)
