#importing the datetime module to display the date and time on which a particular expense was made 
import datetime

#This fuction adds a new expense to the existing list of expenses 
def add_expense():
    #input the description of the expense 
    des = input("Enter the description: ")

    #input the amount spent on that particular expense
    amt = float(input(f"How much have you spent on {des}? "))

    '''Now create a dictionary using the input information. Here strftime() function gives the formatted date on which
    expense was recorded'''
    expense = {"description" : des, "amount" : amt, "date" : datetime.datetime.now().strftime("%d-%b-%Y")}

    #Append the newly created expense to the list of the previous recorded expenses
    expenses.append(expense)
    print("Expense added successfullly")

#This function displays all the undeleted expenses recorded till date 
def view_expenses():
    print("\n----EXPENSE TRACKER----")

    #Display the headings of each column 
    print("\n DESCRIPTION \t AMOUNT \t DATE")
    print("\n")

    #enumerate() displays the expenses by numbering them starting from 1 
    for number,expense in enumerate(expenses, start=1):
        print(f"{number} \t {expense['description']} \t {expense['amount']} \t {expense['date']}")

#This function calculates the total expense - sum of all the exxpenses 
def total_expense():

    #initially sum is initiallized to 0
    sum = 0

    #loop through every expense dictionary in the list and access the corresponding value of the key "amount" in each
    #dictionary and add it to the sum
    for expense in expenses:
        sum += expense["amount"]

    #Print the total expense 
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
               

        



