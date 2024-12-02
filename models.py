from datetime import datetime, date
import calendar

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
            removed = False
            for line in lines:
                columns = line.split(',')
                if int(columns[0]) != id:
                    database.write(line)
                else:
                    removed = True

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
    def display(cls):
        expenses = cls.all()
        
        print('********** EXPENSES **********')
        print(f'{len(expenses)} expense{'' if len(expenses) == 1 else 's'} in total', end='\n\n')
        for expense in expenses:
            print(f'{expense.amount}$ -- {expense.description} -- id: {expense.id} -- date: {expense.created_at.date()}', end=f'{'\n\n' if expense != expenses[-1]  else '\n'}')

class Expense:
    objects = ExpenseManager

    def __init__(self, id, amount, description, created_at):
        self.id = id
        self.amount = float(amount)
        self.description = description
        self.created_at = datetime.strptime(created_at, '%Y-%m-%d')

    @classmethod
    def set_budget(cls, month, budget):
        with open('budgets.csv', 'r') as budgets:
            lines = budgets.readlines()

        with open('budgets.csv', 'w') as budgets:
            for line in lines:
                if month != line.split(',')[0]:
                    budgets.write(line)
                else:
                    budgets.write(f'{month},{budget}\n')
