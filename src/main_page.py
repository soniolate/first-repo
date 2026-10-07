import flet as ft
from datetime import date, datetime
import json
from json.decoder import JSONDecodeError
from pathlib import Path

FILE = Path(__file__).parent / "my expenses.json"
expense_list = []

def menu(page : ft.Page):
    page.title = "menu"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text(
        "Create an expense",
        size=40,
        weight=ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )


    # button add_expense

    def change_to_add_page():
        page.remove(main_container)
        add_expense(page)
        

    button_add_expense = ft.TextButton(
        "Add an expense",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=400,
        on_click=change_to_add_page
    )


    #button check all expense

    def change_to_check_expense():
        page.remove(main_container)
        check_expense(page)
    

    button_check_expense = ft.TextButton(
        "check all expense",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=400,
        on_click=change_to_check_expense
    )


    # button change an expense

    def change_to_change_expense():
        page.remove(main_container)
        change_expense(page)

    button_change_expense = ft.TextButton(
        "Change an expense",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=400,
        on_click=change_to_change_expense
    )



    # button remove an expense

    def change_to_remove_expense():
        page.remove(main_container)
        remove_expense(page)

    button_remove_expense = ft.TextButton(
        "Remove an expense",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=400,
        on_click=change_to_remove_expense
    )


    # button see the stats

    def change_to_stats():
        page.remove(main_container)
        see_stats(page)

    button_see_stats = ft.TextButton(
        "See the stats",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=400,
        on_click=change_to_stats
    )



    main_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(),
                button_add_expense,
                button_check_expense,
                button_change_expense,
                button_remove_expense,
                button_see_stats
                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        border_radius=10,
        bgcolor= ft.Colors.WHITE,
        width=500,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK_38,
            offset=ft.Offset(0,5),
        ),
    )

    page.add(main_container)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def check_expense(page : ft.Page):
    page.title = "Check expenses"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text(
        "Check expenses",
        size=40,
        weight=ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )

    expense_container = ft.Column(
        width=220,
        height=400,
        spacing=10,
        scroll="always",       
    )

    for expense in expense_list:
        expense_text = ft.Text(
            value= f"name : {expense["name"]} \ncategory : {expense["category"]} \namount : {str(expense["amount"])}€ \ndate : {expense["date"]}\n----------------------------------------",
            width=150,
            height=110,
            size=16,

        )
        expense_container.controls.append(expense_text)


    def exit_to_menu():
        page.remove(main_container)
        menu(page)

    exit_button = ft.TextButton(
        "exit",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=200,
        on_click=exit_to_menu
        
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(),
                expense_container,
                exit_button

                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        border_radius=10,
        bgcolor= ft.Colors.WHITE,
        width=500,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK_38,
            offset=ft.Offset(0,5),
        ),
    )

    page.add(main_container)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def change_expense(page : ft.Page):
    page.title = "Change expenses"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    error_message = {
        "name" : "",
        "category" : "",
        "amount" : "",
        "date" : "",
    }

    title = ft.Text(
        "Change an expense",
        size=40,
        weight=ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )

    expenses_container = ft.Column(
        width=220,
        height=400,
        spacing=50,
        scroll="always",
    )

    def change_content(e):
        global expense_list
        if e.control.data[1] == "name":
            expense_list[e.control.data[0]][e.control.data[1]] = e.control.value
        elif e.control.data[1] == "category":
            expense_list[e.control.data[0]][e.control.data[1]] = e.control.value
        elif e.control.data[1] == "amount":
            try:
                expense_list[e.control.data[0]][e.control.data[1]] = float(e.control.value)
            except ValueError:
                e.control.value = ""
        elif e.control.data[1] == "date":
            expense_list[e.control.data[0]][e.control.data[1]] = e.control.value
            try:
                datetime.strptime( e.control.value,"%Y-%m-%d")
            except ValueError:
                is_int = True
                try:
                    if e.control.value != "":
                        int(e.control.value[0])
                    else:
                        is_int = False
                except ValueError:
                    is_int = False
                if len(e.control.value) == 10 and is_int:
                    e.control.value = "The date is wrong"
        
    for i,expense in enumerate(expense_list):
        expense_container = ft.Column(width=220,height=350,)

        name_text = ft.Text(value="Name :")
        expense_container.controls.append(name_text)

        name_field = ft.TextField(label=expense["name"], value=expense["name"], data = (i,"name"), on_change=change_content)
        expense_container.controls.append(name_field)


        category_text = ft.Text(value="Category :")
        expense_container.controls.append(category_text)

        category_field = ft.TextField(label=expense["category"], value=expense["category"], data = (i,"category"),on_change=change_content)
        expense_container.controls.append(category_field)


        amount_text = ft.Text(value="Amount :")
        expense_container.controls.append(amount_text)

        amount_field = ft.TextField(label=expense["amount"], value=expense["amount"], data = (i,"amount"),on_change=change_content)
        expense_container.controls.append(amount_field)


        date_text = ft.Text(value="Date (Y-M-D):")
        expense_container.controls.append(date_text)

        date_field = ft.TextField(label=expense["date"], value=expense["date"], data = (i,"date"),on_change=change_content)
        expense_container.controls.append(date_field)

        expenses_container.controls.append(expense_container)

    def exit_to_menu():
        error = False
        for i in range(len(expenses_container.controls)):
            if expenses_container.controls[i].controls[1].value == "" or expenses_container.controls[i].controls[1].value == "The name cannot be nothing" :
                error_message["name"] = "Empty name"
                expenses_container.controls[i].controls[1].value = "The name cannot be nothing"
                error = True

            if expenses_container.controls[i].controls[3].value == "" or expenses_container.controls[i].controls[3].value == "The name's category cannot be nothing":
                error_message["category"] = "Empty category"
                expenses_container.controls[i].controls[3].value = "The name's category cannot be nothing"
                error = True

            if expenses_container.controls[i].controls[5].value == "" or "-" in str(expenses_container.controls[i].controls[5].value) or expenses_container.controls[i].controls[5].value == "The amount is incorrect":
                error_message["amount"] = "Incorrect amount"
                expenses_container.controls[i].controls[5].value = "The amount is incorrect"
                error = True

            if expenses_container.controls[i].controls[7].value == "":
                error_message["date"] = "The date has to be a real date"
                expenses_container.controls[i].controls[7].value = "The date has to be a real date"
                error = True
            else:
                try:
                    datetime.strptime(expenses_container.controls[i].controls[7].value,"%Y-%m-%d")
                except ValueError:
                    expenses_container.controls[i].controls[7].value = "The date has to be a real date"
                    error_message["date"] = "The date has to be a real date"
                    error = True

        if not error:
            for key in error_message.keys():
                error_message[key] = ""
            save()
            page.remove(main_container)
            menu(page)

    exit_button = ft.TextButton(
        "exit",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=200,
        on_click=exit_to_menu
        
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(),
                expenses_container,
                exit_button,
                ft.Text(value=error_message)

                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        border_radius=10,
        bgcolor= ft.Colors.WHITE,
        width=500,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK_38,
            offset=ft.Offset(0,5),
        ),
    )

    page.add(main_container)


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def remove_expense(page : ft.Page):
    page.title = "Remove expenses"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text(
        "Remove an expense",
        size=40,
        weight=ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )

    expenses_container = ft.Column(
        width=220,
        height=400,
        spacing=-20,
        scroll="always",
    )

    def remove_content(e):
        print(e.control.data)
        for i in range(len(expense_list)):
            if e.control.data == expense_list[i]["id"]:
                del expense_list[i]
                affichage()
                break

    def affichage():
        expenses_container.controls.clear()
        for expense in expense_list:
            
            expense_container = ft.Column(width=220,height=200, spacing= 5)
            expense_text = ft.Text(
                value= f"name : {expense["name"]} \ncategory : {expense["category"]} \namount : {expense["amount"]}€ \ndate : {expense["date"]}",
                size=16
            )
            expense_container.controls.append(expense_text)
            remove_button = ft.Button(
                "Remove",
                data=expense["id"],
                on_click=remove_content
            )
            expense_container.controls.append(remove_button)        
            expenses_container.controls.append(expense_container)

    def exit_to_menu():
        save()
        page.remove(main_container)
        menu(page)

    exit_button = ft.TextButton(
        "exit",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=200,
        on_click=exit_to_menu
        
    )
    affichage()
    main_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(),
                expenses_container,
                exit_button

                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0
        ),
        padding=20,
        border_radius=10,
        bgcolor= ft.Colors.WHITE,
        width=500,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK_38,
            offset=ft.Offset(0,5),
        ),
    )

    page.add(main_container)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def see_stats(page : ft.Page):
    page.title = "Stats"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    title = ft.Text(
        "Stats",
        size=40,
        weight=ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )

    expenses_container = ft.Column(
        width=220,
        height=400,
        spacing=15,
        scroll="always",
    )



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
            "amount" : 0.0
            }
        expenses_container.controls.append(ft.Text(value=f"You spent a total of {total:.2f}€"))
        expenses_container.controls.append(ft.Text(value=f"You spent an average of {(total/len(expense_list)):.2f}€"))

        expenses_container.controls.append(ft.Text(value=f"You did {len(expense_list)} expense(s)"))
        for expense in expense_list:
            if expense["amount"] > max_expense["amount"]:
                max_expense = expense
        expenses_container.controls.append(ft.Text(value=f"Your biggest expense is {max_expense['name']} : {max_expense['amount']}€\nCategory : {max_expense['category']}\nDate : {max_expense['date']}"))
        expenses_container.controls.append(ft.Text(value=", \n".join(f"{expense} : {amount:.2f}€" for expense, amount in category_amount.items())))
    else:
        expenses_container.controls.append(ft.Text(value="You did no expenses"))


    
    def exit_to_menu():
        page.remove(main_container)
        menu(page)

    exit_button = ft.TextButton(
        "exit",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
        width=200,
        on_click=exit_to_menu
        
    )

    main_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(),
                expenses_container,
                exit_button

                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        border_radius=10,
        bgcolor= ft.Colors.WHITE,
        width=500,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK_38,
            offset=ft.Offset(0,5),
        ),
    )

    page.add(main_container)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def add_expense(page : ft.Page):
    page.title = "Create an expense"
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER



    title = ft.Text(
        "Create an expense",
        size=40,
        weight=ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )





    expense_container = ft.Row(spacing=10, alignment=ft.CrossAxisAlignment.CENTER)


    # text field for the name of the expense

    expense_name = ft.TextField(
        label="name of the expense"
    )
    expense_container.controls.append(expense_name)

    # text field for the category's name of the expense
    category_text = ft.TextField(
        label="Category's name of the expense"
    )

    expense_container.controls.append(category_text)
   # expense_container.controls.append(category_bar)

    # the field text where the user tapes the expense

    def text_field_change(e):
        for i in range(len(field_text.value)):
            if not field_text.value[i] in "0123456789,.":
                field_text.value = ""                


    field_text = ft.TextField(
        label="expense",
        on_change=text_field_change
    )

    expense_container.controls.append(field_text)

    #submit button

    def submit(e):
        if field_text.value == "" or field_text.value == "Put an amount before submit":
            field_text.value = "Put an amount before submit"
        elif expense_name.value == "" or expense_name.value == "Put a name for the category before submit":
            expense_name.value = "Put a name before submit"
        elif category_text.value == "" or category_text.value == "Put a name for the category before submit":
            category_text.value = "Put a name for the category before submit"
        else:

            field_text.value = field_text.value.replace(",", ".")

            if len(expense_list) != 0:
                expense_id = max(expense["id"] for expense in expense_list) + 1
            else:
                expense_id = 0
            expense_date = str(date.today())
            expense = {
                "id" : expense_id,
                "name" : expense_name.value,
                "category" : category_text.value,
                "amount" : float(field_text.value),
                "date" : expense_date,
                }

            expense_list.append(expense)
            print(expense_list)
            save()
            page.remove(main_container)
            menu(page)

    submit_button = ft.IconButton(
        icon=ft.Icons.PLAY_ARROW,
        on_click=submit

    )

    expense_container.controls.append(submit_button)


    main_container = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(),
                expense_container,
                

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=20,
        border_radius=10,
        bgcolor= ft.Colors.WHITE,
        width=1000,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.BLACK_38,
            offset=ft.Offset(0,5),
        ),
    )

    page.add(main_container)


def reset():
    global expense_list
    expense_list = []
    with open(FILE,"w", encoding="utf-8") as f:
        json.dump(expense_list, f, ensure_ascii=False, indent=4)

def save():
    with open(FILE,"w", encoding="utf-8") as f:
        json.dump(expense_list, f, ensure_ascii=False, indent=4)

def load():
    global expense_list
    try:
        with open(FILE, encoding="utf-8") as f:
            expense_list = json.load(f)
    except FileNotFoundError:
        print("not found")
        expense_list = []
    except JSONDecodeError:
        expense_list = []
        print("not correct")

load()
ft.run(menu)