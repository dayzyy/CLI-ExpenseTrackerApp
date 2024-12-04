from datetime import datetime, date
import calendar

month_names = calendar.month_name[1:]
months = {}

def unknown_month(n):
    if n < 1 or n > 12 :
        suffix = 'th'
        _n = abs(n) % 10
        match _n:
            case -1: suffix = 'st'
            case -2: suffix = 'nd'
            case -3: suffix = 'rd'
            case _: pass

        print(f'{n}{suffix} month is unknown to humanity!')
        return True
    else:
        return False

for i in range(12):
    months[i + 1] = month_names[i]

class ExpenseManager:
    # Checks if databse (db.csv) file already exists. If it doesnt, the function creates it. Does the same for budgets.csv
    @classmethod
    def database(cls):
        try:
            open('db.csv', 'r')

            try:
                open('id_counter_file.txt', 'r')

            except FileNotFoundError:
                with open('id_counter_file.txt', 'w') as counter:
                    counter.write(str(len(cls.all())))

        except FileNotFoundError:
            open('db.csv', 'w')

            with open('id_counter_file.txt', 'w') as counter:
                counter.write('0')

        try:
            open('budgets.csv', 'r')
        except FileNotFoundError:
            with open('budgets.csv', 'w') as budgets:
                months = calendar.month_name[1:]
                for month in months:
                    budgets.write(f'{month},N/A\n')

    
    # Saves a new Expense instance into the database
    @classmethod
    def create(cls, amount, description):
        with open('id_counter_file.txt', 'r') as database: 
            id_data = database.read().strip()
            id = int(id_data.replace('\n', ''))
        with open('id_counter_file.txt', 'w') as database: 
            database.write(str(id + 1))

        created_at = date.today()

        with open('db.csv', 'a') as database:
            database.write(f'{id},{amount},{description},{created_at}\n')

    # Removes data of Expense linked to the provided ID
    @classmethod
    def remove(cls, id):
        with open('db.csv', 'r') as database:
            lines = database.readlines()
            
        with open('db.csv', 'w') as database:
            for line in lines:
                columns = line.split(',')
                if int(columns[0]) != id:
                    database.write(line)

    # Returns all the Expense instances from the database
    @classmethod
    def all(cls):
        expenses_data = [] # Raw data from csv
        expenses = [] # Actual Expense instances
        with open('db.csv', 'r') as database:
            for line in database:
                expenses_data.append(line.split(','))

        for expense_data in expenses_data:
            expense_data[-1] = expense_data[-1].replace('\n', '')
            expenses.append(Expense(*expense_data))

        return expenses

    @classmethod
    def DoesNotExist(cls, id):
        expneses = cls.all()

        for expense in expneses:
            if expense.id == id:
                return False
        print(f'ValueError: No expense with id: {id}!')
        return True
    
    # Returns summray of expenses for specified month. If month=0 is left to default it returns summary of expenses throughout the whole year
    @classmethod
    def summary(cls, month=0):
        expenses = cls.all()
        summary = 0

        if month == 0:
            for expense in expenses:
                summary += expense.amount
            return summary

        for expense in expenses:
            if expense.created_at.month == month:
                summary += expense.amount

        return summary

    @classmethod
    def display(cls, month=None):
        expenses = cls.all()

        match month:
            case None:
                with open('budgets.csv', 'r') as budgets:
                    lines = budgets.readlines()

                budget_this_month = 'N/A'
                for line in lines:
                    if line.strip().split(',')[0] == months[date.today().month]:
                        budget_this_month = line.strip().split(',')[1]

                expenses_this_month = []
                for expense in expenses:
                    if expense.created_at.month == date.today().month:
                        expenses_this_month.append(expense)

                print('**********EXPENSES THIS MONTH**********')
                print(f'{len(expenses_this_month)} expense{'' if len(expenses_this_month) == 1 else 's'} in total', end='\n\n')
                for expense in expenses_this_month:
                    print(f'{expense.amount}$ -- {expense.description} -- id: {expense.id} -- date: {expense.created_at.date()}', end='\n\n')

                spent = cls.summary(month=date.today().month)

                print(f'Budget this month: {budget_this_month}{'$' if budget_this_month != 'N/A' else ''}')
                print(f'Spent: {spent}$')

                if budget_this_month != 'N/A':
                    if int(budget_this_month) - spent > 0:
                        print(f'Money left to spend: {int(budget_this_month) - spent}$')
                    elif int(budget_this_month) - spent < 0:
                        print(f'WARNING!: You have exceeded your monthly budget by {int(budget_this_month) - spent}$')


            case 'all':
                print('**********EXPENSES THIS YEAR**********')
                print(f'{len(expenses)} expense{'' if len(expenses) == 1 else 's'} in total', end='\n\n')
                for expense in expenses:
                    print(f'{expense.amount}$ -- {expense.description} -- id: {expense.id} -- date: {expense.created_at.date()}', end=f'{'\n\n' if expense != expenses[-1]  else '\n'}')

            case _:
                with open('budgets.csv', 'r') as budgets:
                    lines = budgets.readlines()

                budget_this_month = 'N/A'
                for line in lines:
                    if line.strip().split(',')[0] == months[month]:
                        budget_this_month = line.strip().split(',')[1]

                expenses_for_month = []
                for expense in expenses:
                    if expense.created_at.month == month:
                        expenses_for_month.append(expense)

                spent = cls.summary(month=month)

                print(f'**********EXPENSES IN {months[month].upper()}**********')
                print(f'{len(expenses_for_month)} expense{'' if len(expenses_for_month) == 1 else 's'} in total', end='\n\n')
                for expense in expenses_for_month:
                    print(f'{expense.amount}$ -- {expense.description} -- id: {expense.id} -- date: {expense.created_at.date()}', end='\n\n')
                print(f'Budget this month: {budget_this_month}{'$' if budget_this_month != 'N/A' else ''}')
                print(f'Spent: {spent}$')

                if budget_this_month != 'N/A':
                    if int(budget_this_month) - spent > 0:
                        print(f'Money left to spend: {int(budget_this_month) - spent}$')
                    elif int(budget_this_month) - spent < 0:
                        print(f'WARNING!: You have exceeded your monthly budget by {int(budget_this_month) - spent}$')

class Expense:
    objects = ExpenseManager

    def __init__(self, id, amount, description, created_at):
        self.id = id
        self.amount = float(amount)
        self.description = description
        self.created_at = datetime.strptime(created_at, '%Y-%m-%d')
    
    # Sets a budget for the specified month. If left to default, sets budget for the current month
    @classmethod
    def set_budget(cls, budget, month=months[date.today().month]):
        with open('budgets.csv', 'r') as budgets:
            lines = budgets.readlines()

        with open('budgets.csv', 'w') as budgets:
            for line in lines:
                if month != line.split(',')[0]:
                    budgets.write(line)
                else:
                    budgets.write(f'{month},{budget}\n')
