import argparse
import calendar

from models import  Expense, ExpenseManager

ExpenseManager.database()

month_names = calendar.month_name[1:]
months = {}

for i in range(12):
    months[i + 1] = month_names[i]

parser = argparse.ArgumentParser(description='Manage your expenses')

subparser = parser.add_subparsers(dest='command', help='Available commands')

add_parser = subparser.add_parser('add', help='Add a new expense')
add_parser.add_argument('-d', '--description', type=str, help='Description of the expense', required=True)
add_parser.add_argument('-a', '--amount', type=float, help='Amount of the expense', required=True)

delete_parser = subparser.add_parser('delete', help='Delete an archived expense by providing its ID')
delete_parser.add_argument('--id', type=int, help='ID  of the expense to delete')

list_parser = subparser.add_parser('list', help='List all the expenses')

summary_parser = subparser.add_parser('summary', help='See the summary of your expenses')
summary_parser.add_argument('-m', '--month', type=int, help='Select a month to see expenses specific for it', required=False)

budget_parser = subparser.add_parser('budget', help='Manage your monthly budgets')

budget_subparser = budget_parser.add_subparsers(dest='budget_command', help='Available  commands')
set_parser = budget_subparser.add_parser('set', help='Set a new budget for certain month')
set_parser.add_argument('-m', '--month', type=int, help='Month to set the budget for', required=True)
set_parser.add_argument('-a', '--amount', type=int, help='Amount of the budget', required=True)


args = parser.parse_args()
print(args)

match args.command:
    case 'add':
        Expense.objects.create(args.amount, args.description)
    case 'list':
        Expense.objects.display()
    case 'delete':
        Expense.objects.remove(args.id)
    case 'summary':
        if args.month == None:
            print(f'Summary of all expenses: {Expense.objects.summary()}$')
        else:
            print(f'Summary of expenses in {months[args.month]}: {Expense.objects.summary(month=args.month)}$')
    case 'budget':
        if args.budget_command == 'set':
            Expense.set_budget(months[args.month], args.amount)
