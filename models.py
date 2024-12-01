from datetime import date

class ExpenseManager:
    # Checks if databse (db.csv) file already exists. If it doesnt, the function creates it.
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
            database.write(f'{id}, {amount}, {description}, {created_at}\n')

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
    def display(cls):
        expenses = cls.all()
        
        print('********** EXPENSES **********')
        print(f'{len(expenses)} expense{'' if len(expenses) == 1 else 's'} in total', end='\n\n')
        for expense in expenses:
            print(f'{expense.amount}$ -- {expense.description} -- id: {expense.id} -- date: {expense.created_at}', end=f'{'\n\n' if expense != expenses[-1]  else '\n'}')

class Expense:
    objects = ExpenseManager

    def __init__(self, id, amount, description, created_at):
        self.id = id
        self.amount = amount
        self.description = description
        self.created_at = created_at
