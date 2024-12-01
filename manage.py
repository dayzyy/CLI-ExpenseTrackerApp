import argparse

from models import  Expense, ExpenseManager

ExpenseManager.database()

parser = argparse.ArgumentParser(description='Manage your expenses')

subparser = parser.add_subparsers(dest='command', help='Available commands')

add_parser = subparser.add_parser('add', help='Add a new expense')
add_parser.add_argument('-d', '--description', type=str, help='Description of the expense', required=True)
add_parser.add_argument('-a', '--amount', type=float, help='Amount of the expense', required=True)

args = parser.parse_args()
print(args)

if args.command == 'add':
    Expense.objects.create(args.amount, args.description)
