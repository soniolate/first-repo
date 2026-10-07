from datetime import date, datetime
import json
from json.decoder import JSONDecodeError

expense_list = []
leave = False

def create_expense():
    expense_amount = 0.00
    while True:
        expense_name = input("What's the name of the expense ?\n")
        if expense_name == "":
            print("The name can't be nothing")
        else:
            break 
    while True:
        try:
            expense_amount = float(input("What's the amount of the expense ?\n"))
            if expense_amount < 0:
                print("the amount can't be negative")
            else:
                break
        except ValueError :
            print("Please enter the amount")
    while True:
        expense_category = input("What's the expense's category ?\n")
        if expense_category == "":
            print("the category's name can't be nothing")
        else:
            break
    expense_date = input("It's a new or an old expense ? (y/n)\n").lower()
    if expense_date == "y":
        expense_date = str(date.today())
    elif expense_date == "n":
        while True:
            try:
                expense_date = input("When was the expense ? (y-m-d)\n")
                datetime.strptime(expense_date,"%Y-%m-%d")
                break
            except ValueError:
                print("The date is wrong")

    
    if expense_list:
        new_id = max(expense["id"] for expense in expense_list) + 1
    else:
        new_id = 0

    expense = {
        "id" :new_id,
        "name":expense_name,
        "amount":expense_amount,
        "category":expense_category,
        "date":expense_date
    }
    print(expense)
    return expense

def see_expenses():
    print("=======EXPENSES========")
    print("ID   Name   Amount    Category     Date")
    for expense in expense_list:
        print(expense["id"],end= "  ")
        print(expense["name"],end= "  ")
        print(str(expense["amount"]) + "€",end= "  ")
        print(expense["category"],end= "  ")
        print(expense["date"],end= "\n\n")
        


def edit_expense():
    see_expenses()
    while True:
        try:
            i = int(input("Which expense would you like to edit ? (type the id)\n"))
            break
        except ValueError:
            print("Please enter a valid id")

    found = False
    for expense in expense_list:
        if expense["id"] == i:
            found = True
            print(expense)
            truc = input("What would you like to change ?\n" \
            "1-Name\n" \
            "2-Amount\n" \
            "3-Category\n" \
            "4-Date\n")
            if truc == "1":
                new_name = input("What's the new name ?\n")
                expense["name"] = new_name
            elif truc == "2":
                while True:
                    try:
                        new_amount = float(input("What's the new amount ?\n"))
                        if new_amount < 0:
                            print("the amount can't be negative")
                        else:
                            break
                    except ValueError:
                        print("Please enter the amount")
                expense["amount"] = new_amount
            elif truc == "3":
                new_category = input("What's the new category ?\n")
                expense["category"] = new_category
            elif truc == "4":
                new_date = input("What's the new date ?\n")
                expense["date"] = new_date
            break
    if not found:
        print("Expense not found")


def remove_expense():
    see_expenses()
    while True:
        try:
            expense_id = int(input("Which expense would you like to remove ? (type the id)\n"))
            break
        except ValueError:
            print("Please enter a valid id")

    found = False
    for i in range(len(expense_list)):
        if expense_list[i]["id"] == expense_id:
            del expense_list[i]
            found = True
            break
    if not found:
        print("Expense not found")


def stats():
    if expense_list:
        category_amount = {}

        for expense in expense_list:
            category = expense["category"]
            amount = expense["amount"]

            if category not in category_amount:
                category_amount[category] = 0
            category_amount[category] += amount

        total = sum(expense["amount"] for expense in expense_list)
        max_expense = {
            "amount" : 0
            }
        print(f"You spent a total of {total}€")
        print(f"You spent an average of {total/len(expense_list)}€")

        print(f"You did {len(expense_list)} expense(s)")
        for expense in expense_list:
            if expense["amount"] > max_expense["amount"]:
                max_expense = expense
        print(f"Your biggest expense is {max_expense['name']} : {max_expense['amount']}€\nCategory : {max_expense['category']}\nDate : {max_expense['date']}")
        print("-----------Category's stats------------")
        print(", \n".join(f"{expense} : {amount:.2f}" for expense, amount in category_amount.items()))
    else:
        print("You did no expenses")

  
        


def menu():
    global leave
    choose = input("What do you want to do ?\n"
    "1-Create an expense\n"
    "2-See the expenses\n"
    "3-Edit an expense\n"
    "4-Remove an expense\n"
    "5-See the statistics\n"
    "6-Leave\n"
    "7-Reset\n")
    if choose == "1":
        expense_list.append(create_expense())
        save()
    elif choose == "2":
        see_expenses()
    elif choose == "3":
        edit_expense()
        save()
    elif choose == "4":
        remove_expense()
        save()
    elif choose == "5":
        stats()
    elif choose == "6":
        save()
        leave = True
    elif choose == "7":
        reset()


def reset():
    global expense_list
    expense_list = []
    with open("my expenses.json","w", encoding="utf-8") as f:
        json.dump(expense_list, f, ensure_ascii=False, indent=4)





def save():
    with open("my expenses.json","w", encoding="utf-8") as f:
        json.dump(expense_list, f, ensure_ascii=False, indent=4)

def load():
    global expense_list
    try:
        with open("my expenses.json", encoding="utf-8") as f:
            expense_list = json.load(f)
    except FileNotFoundError:
        expense_list = []
    except JSONDecodeError:
        expense_list = []
    


load()
while not leave:
    menu()