import argparse

from models import  Expense, ExpenseManager

ExpenseManager.database()

parser = argparse.ArgumentParser(description='Manage your expenses')

subparser = parser.add_subparsers(dest='command', help='Available commands')

add_parser = subparser.add_parser('add', help='Add a new expense')
add_parser.add_argument('-d', '--description', type=str, help='Description of the expense', required=True)
add_parser.add_argument('-a', '--amount', type=float, help='Amount of the expense', required=True)

delete_parser = subparser.add_parser('delete', help='Delete an archived expense by providing its ID')
delete_parser.add_argument('id', type=int, help='ID  of the expense to delete')

list_parser = subparser.add_parser('list', help='List all the expenses')


args = parser.parse_args()
print(args)

match args.command:
    case 'add':
        Expense.objects.create(args.amount, args.description)
    case 'list':
        Expense.objects.display()
    case 'delete':
        Expense.objects.remove(args.id)
