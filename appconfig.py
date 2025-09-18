import json
import os

# Define a function to add an expense
def add_expense(expense):
  # Save expense to a file
  with open('expenses.json', 'a') as f:
    json.dump(expense, f)
    f.write('\n')

# Define a function to calculate total expenses
def calculate_total_expenses():
  # Load expenses from file
  with open('expenses.json', 'r') as f:
    expenses = [json.loads(line) for line in f.readlines()]
  total = sum(expense['expense'] for expense in expenses)
  return total

# Define a function to get user input
def get_user_input():
  # Create a readline interface for user input
  import readline
  expense = input('Enter expense (e.g., {"expense": 10.99, "category": "Food"}): ')
  try:
    expense = json.loads(expense)
  except json.JSONDecodeError:
    print('Invalid JSON input. Please try again.')
    return get_user_input()
  return expense

# Main function
def main():
  while True:
    # Get user input
    expense = get_user_input()
    add_expense(expense)
    print(f'Expense added successfully! Total expenses: ${calculate_total_expenses():.2f}')

if __name__ == '__main__':
  main()
