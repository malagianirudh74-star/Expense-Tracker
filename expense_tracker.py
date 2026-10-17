#importing the datetime module to display the date and time on which a particular expense was made 
import datetime

def add_expense():
    des = input("Enter the description: ")
    amt = float(input(f"How much have you spent on {des}? "))
    expense = {"description" : des, "amount" : amt, "date" : datetime.datetime.now().strftime("%d-%b-%Y")}
    expenses.append(expense)
    print("Expense added successfullly")

def view_expenses():
    print("\n----EXPENSE TRACKER----")
    print("\n DESCRIPTION \t AMOUNT \t DATE")
    print("\n")
    for number,expense in enumerate(expenses, start=1):
        print(f"{number} \t {expense['description']} \t {expense['amount']} \t {expense['date']}")

def total_expense():
    sum = 0
    for expense in expenses:
        sum += expense["amount"]
    print("Total expense is: ",sum)

def ask_to_continue():
    ch = int(input("do you want to continue? \n1.Yes \n2.No \nEnter 1 or 2: "))
    return ch                

expenses = []

while True:
    print("1. Add Expense")
    print("2. View Expense")
    print("3. Compute Total Expense")
    print("4. Exit")

    ch = int(input("Enter your choice: "))

    if ch == 1:
        while True:
            add_expense()
            ch = ask_to_continue()
            if ch == 1:
                continue
            else:
                break

    elif ch == 2:
        view_expenses()

    elif ch == 3:
        total_expense()

    elif ch == 4:
        print("Exiting - Thank You")
        break

    else:
        print("Invalid number, try again")
               

        



