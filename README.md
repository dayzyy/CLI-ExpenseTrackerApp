# Expense Manager CLI Application

Using this application you can **create** and **delete** expneses, as well as **set a budget** for each month. Afterwards you can display them and keep track of your expenses throughout the whole year. 
If you go over your budget for the current month the application will warn you.

## Features
- Add new expenses
- Delete an expense
- Set a budget for each month
- See the summary of your expeneses base on a month

## Prerequisites
- **Python 3.6+**
- No External Modules Required

## Setup
1. Clone the repository:
```
git clone https://github.com/dayzyy/CLI-ExpenseTrackerApp.git
```
2. Navigate to the created directory:
```
cd CLI-ExpenseTrackerApp/
```

You are all set! Now you can interact with the app using commands listed below  
You can also use the comand line to see all available commands:
```python
python3 manage.py -h
```

## commands

```python
# To add an expense
python3 manage.py add --description <description> --amount <amount>
python3 manage.py add -d <description> -a <amount>

# Example
python3 manage.py add --description 'Lunch' --amount 2.99
python3 manage.py add -d 'Lunch' -a 2.99

# To delete an expense
python3 manage.py delete --id <id>

# Example
python3 manage.py delete --id 1

# To set a budget for a month
python3 manage.py budget set --month <month> --amount <amount>
python3 manage.py budget set -m <month> -a <amount>

# Examples
python3 manage.py set --amount 2000 # Sets the budget for the current month, if  <month> arguement is not provided
python3 manage.py set --month 10 --amount 2000 # Sets the budget for the 10th month(October)
python3 manage.py set -m 7 -a 500 # Sets the budget for the 7th month(July)

# To display expenses based on month
python3 manage.py list <month>

# Examples
python3 manage.py list # Displays expenses for the current month, if the <month> arguement is not provided
python3 manage.py list --month 12 # Displays expenses for the 12th month(December)
python3 manage.py list -m 1 # Displays expenses for the 1st month(Jenuary)

# To display the summary of expenses based on month
python3 manage.py summary  <month>

# Examples
python3 manage.py summary # Displays the summary of expenses for the current month, if the <month> arguement is not provided
python3 manage.py summary --month 12 # Displays the summary of expenses for the 12th month(December)
python3 manage.py summary -m 1 # Displays the summary of expenses for the 1st month(Jenuary)
```

### Inspired By
**roadmap.sh** https://roadmap.sh/projects/expense-tracker
