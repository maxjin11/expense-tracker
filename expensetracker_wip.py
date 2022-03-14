"""
Add a feature to analyze expenses on a per-monthly basis, and comparing the results of one month to the next.

Instead of separate buttons in the analyze and view menus, just use a dropdown instead.

Export database table to an excel spreadsheet

Create bar graphs for month-to-month comparisons, pie graphs for comparisons between categories
"""

# used to track the dates of expenses
from datetime import date
from datetime import time
from datetime import datetime

# used to track periods of time using date math
from datetime import timedelta

# used to keep track of the expenses after exiting the program
import sqlite3
from sqlite3 import Error

# used to create the GUI
from tkinter import *
from tkinter import ttk

# main use: time.sleep() to create useful delays
import time as t

# used to calculate statistics regarding expenses during a period of time
import statistics

# used to convert background images files
from PIL import Image

import os.path
from os import path

from tkcalendar import Calendar

# creates a connection to the sqlite database
def create_connection(path):
    try:
        global c
        c = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return c

# Each of these buttons update the scene variable, so when the GUI is refreshed
# using menu(), the GUI displays something different, depending on the button pressed
def addExpense():
    global scene 
    scene = 1
    menu()
    
def deleteExpense():
    global scene
    scene = 2
    menu()

def viewExpenses():
    global scene
    scene = 3
    menu()

def analyzeExpenses():
    global scene
    scene = 4
    menu()

# this simply exits the program
def exitProgram():
    window.destroy()

# TODO: experiment using a function that serves as a button template, so when changes need to be made to every button, they do not need to be dont multiple times.
def button_temp(text, function, fontsize, fontcolor, height, width, xcoord, ycoord):
    tempButton = Button(window, text=text, height=height, width=width, font=("Helvetica", fontsize), command=function)    
    tempButton.config(borderwidth=0, fg=fontcolor, relief=RAISED)
    tempButton.configure(highlightbackground=charcoal)
    tempButton.place(x=xcoord, y=ycoord)
        
def addLabels(text, fontsize, xcoord, ycoord):
    addLabel = Label(window, text=text, bg=charcoal, fg=cream, font=("Helvetica", fontsize))
    addLabel.place(x=xcoord, y=ycoord)

# this is the back button, which sets the scene variable to 0, then refreshes the screen using menu(). 
# this returns you back to the default menu.
def menuButton():
    def back():
        global scene
        scene = 0
        menu()

    button_temp("Back to Menu", lambda: back(), 14, charcoal, 2, 12, 800, 460)
    # back_menu = Button(window, text="Back to Menu", padx=20, pady=15, command=lambda: back())
    
    # if scene == 3:
        # back_menu.grid(row=0, column=0)
    
    # else:
        # back_menu.pack()
    # back_menu.place(x=800, y=450)

# this creates another window that displays a short message, which changes depending on the button pressed.
# it checks the scene variable before displaying a message to decide which message to display
def popup():
    popup = Toplevel()
    popup.title("Confirmation")
    if scene == 1:
        popupmsg = "Your expense has successfully been added."
    elif scene == 2:
        popupmsg = "Your expense(s) have successfully been deleted."

    popuplabel = Label(popup, text=popupmsg)
    popuplabel.grid(row=0, column=0)

# sets the connection variable to None until the create_connection function is called.
c = None

#sets the default value of the scene variable; 0.
scene = 0

# creates the window, resizes it to 960x540, then limits the capability of resizing the window.
# this is done to keep the proportions of the program in check.
window = Tk()
window.geometry("960x540")
window.resizable(height=False, width=False)

# creates the connection to the sqlite database.
create_connection("expenses.db")

# sets the cursor object in order to operate on the database
cur = c.cursor()

# creates a table if it does not exist already.
# it sets 4 columns; and ID, which automatically increments with each added expense, the value, the purpose, and the date.
cur.execute("CREATE TABLE IF NOT EXISTS IDExpenses (ID INTEGER PRIMARY KEY AUTOINCREMENT, Name, Value, Purpose, Date)")

# title
title = Label(window, text="Expense Tracker")

# sets similar menu systems to the one that used the scene variable. 
# filter is used in the view expenses structure (elif scene == 3)
filter = 0

# analyze is used in the analyze expenses structure (elif scene == 4)
analyze = 0
flag = 0
entry_break = 0
charcoal = "#273043"
lightred = "#F02D3A"
cream = "#EFF6EE"
now = datetime.now()

# checks if the correct background image exists, and if not, it converts the jpg version of that file.
"""
if path.exists("bglandscape.png") == False:
    img0 = Image.open("background/bglandscape.jpg")
    img1 = img0.resize((960, 540))
    img1.save("background/bglandscape.png")


def background():
    bg_image = PhotoImage(file="background/bglandscape.png")
    bg_label = Label(window, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
"""

# displays the widgets which make up the GUI, what it displays changes depending on the value of the scene variable
# since it changes depending on the variable, this function can be used to refresh the GUI.
# this is important since the refresh can be used to update the database information displayed.

def menu():
    # default menu
    if scene == 0:
        # destroys all the previous widgets, this is how the refresh function is possible
        for widget in window.winfo_children():
            widget.destroy()

        window.config(background=charcoal)

        # background()
        # add_image = PhotoImage(file="buttons/add_btn.png")

        # various buttons for different purposes
        """
        addButton = Button(window, text="Add Expense", height=2, width=15, font="bold_font", command=lambda: addExpense())    
        addButton.config(borderwidth=0, fg=charcoal, relief=RAISED)
        addButton.configure(highlightbackground=charcoal)
        addButton.place(x = 54, y = 50) # width is 122? height is 73?
        
        delButton = Button(window, text="Delete Expense", height=2, width=15,  font="bold_font", command=lambda: deleteExpense())
        delButton.config(borderwidth=0, fg=charcoal, relief=RAISED)
        delButton.configure(highlightbackground=charcoal)
        delButton.place(x = 54, y = 130)

        viewButton = Button(window, text="View Expenses", height=4, width=20, command=lambda: viewExpenses())
        viewButton.place(x = 54, y = 210)

        analyzeButton = Button(window, text="Analyze Expenses", height=4, width=20, command=lambda: analyzeExpenses())
        analyzeButton.place(x = 54, y = 290)

        exitButton = Button(window, text="Exit Program", height=4, width=20, command=lambda: exitProgram())
        exitButton.place(x = 54, y = 370)

        """

        button_temp("Add Expense", lambda: addExpense(), 14, charcoal, 2, 15, 54, 50)
        button_temp("Delete Expense", lambda: deleteExpense(), 14, charcoal, 2, 15, 54, 130)
        button_temp("View Expenses", lambda: viewExpenses(), 14, charcoal, 2, 15, 54, 210)
        button_temp("Analyze Expenses", lambda: analyzeExpenses(), 14, charcoal, 2, 15, 54, 290)
        button_temp("Exit Program", lambda: exitProgram(), 14, lightred, 2, 15, 54, 370)


    # expense addition menu
    elif scene == 1:
        for widget in window.winfo_children():
            widget.destroy()

        # background()

        # variables used to set defaults and to manage the inputted values 
        day_tkvar = StringVar(window)
        month_tkvar = StringVar(window)
        purpose_tkvar = StringVar(window)
        name_tkvar = StringVar(window)
        value_tkvar = StringVar(window)
        year_tkvar = StringVar(window)
        
        # setting default values
        day_tkvar.set(1)
        month_tkvar.set(1)
        purpose_tkvar.set("Miscellaneous")
        
        # setting possible options for dropdowns
        days = range(1, 32)
        months = range(1, 13)
        purpose = {"Miscellaneous", "Rent", "Dining", "Clothing", 
                   "Entertainment", "Technology", 
                   "Utilities", "Groceries", "Loans"}
        
        # dropdown widgets
        dayMenu = OptionMenu(window, day_tkvar, *days)
        monthMenu = OptionMenu(window, month_tkvar, *months)
        purposeMenu = OptionMenu(window, purpose_tkvar, *purpose)
        
        # text entry widgets
        name = Entry(window, textvariable=name_tkvar)
        value = Entry(window, textvariable=value_tkvar)
        year = Entry(window, textvariable=year_tkvar)
        
        # labels for each entry system
        addLabels("Name:", 11, 97, 24)
        addLabels("Value:", 11, 100, 46)
        addLabels("Day:", 11, 109, 72)
        addLabels("Month:", 11, 97, 104)
        addLabels("Year:", 11, 105, 131)
        addLabels("Purpose:", 11, 80, 156)
        # add calendar date selector widget

        # displays the widgets on the screen
        name.place(x=150, y=30)
        value.place(x=150, y=50)
        dayMenu.place(x=150, y=70)
        monthMenu.place(x=150, y=102)
        year.place(x=150, y=134)
        purposeMenu.place(x=150, y=154)


        def select_date():
            print(cal.selection_get())
            print("Day:", int(str(cal.selection_get())[8:10]))
            print("Month:", cal.get_displayed_month()[0])
            print("Year:", cal.get_displayed_month()[1])
            day_tkvar.set(int(str(cal.selection_get())[8:10]))
            month_tkvar.set(int(cal.get_displayed_month()[0]))
            year_tkvar.set(int(cal.get_displayed_month()[1]))

        cal = Calendar(window, selectmode="day", year=now.year, month=now.month, day=now.day, firstweekday="sunday")
        cal.place(x=400, y=50)

        button_temp("Select Date", lambda: select_date(), 11, charcoal, 3, 10, 655, 50)
        
        # this retrieves the inputted information from the drop downs and entry widgets
        def get_info():
            name_info = str(name_tkvar.get())
            value_info = float(value_tkvar.get())
            day_info = int(day_tkvar.get())
            month_info = int(month_tkvar.get())
            year_info = int(year_tkvar.get())
            purpose_info = purpose_tkvar.get()
            
            # sets the retrieved date data into an actual date object
            expensedate = str(date(year_info, month_info, day_info))
            
            # variables are inserted into a tuple to be inserted into an sqlite table
            variables = (value_info, purpose_info, expensedate)
            cur.execute("INSERT INTO IDExpenses VALUES (?, ?, ?, ?, ?)", (None, name_info, value_info, purpose_info, expensedate))
            c.commit()
            print("The addition of the expense was successful.")
            
            # the confirmation window pops up
            popup()
        
        button_temp("Submit", lambda: get_info(), 11, lightred, 2, 10, 150, 190)   
        

        menuButton()

    # expense deletion menu
    elif scene == 2:
        for widget in window.winfo_children():
            widget.destroy()

        # background()

        # column names for the table
        columns = ("ID, Name, Value, Purpose, Date")

        # creates a table object which displays the expenses in the database
        # IMPORTANT: tkinter tables that do not use treeview are not usable, because the table must have selectable values.
        # this is needed in order to select which values to delete from the table.
        treetable = ttk.Treeview(window, height = 15, show="headings", column=columns)
        
        # column headings
        treetable.heading("#1", text="ID")
        treetable.heading("#2", text="Name")
        treetable.heading("#3", text="Value")
        treetable.heading("#4", text="Purpose")
        treetable.heading("#5", text="Date")
        
        treetable.column("#1", width=160)
        treetable.column("#2", width=160)
        treetable.column("#3", width=160)
        treetable.column("#4", width=160)
        treetable.column("#5", width=160)

        # retrieves information from the sqlite database; IDExpenses table
        # retrieves up to 15 entries

        # this selects the entries
        cur.execute("SELECT * FROM IDExpenses LIMIT 0, 15")
        # stores the selected entries in a variable and fetches them
        expenses = cur.fetchall()
        
        # inserts the entries into the treetable
        for row in expenses:
            treetable.insert("", END, values=row)
        
        # displays the treetable on the screen
        treetable.place(x=80, y=5)

        print("Table successfully displayed.")
        
        # deletes every entry in IDExpenses
        def clearTable():
            cur.execute("DELETE FROM IDExpenses")
            print("Table successfully cleared.")
            c.commit()
            # refreshes the table view
            menu()
            # confirmation window
            popup()
            
        # deletes the entries that are selected
        def deleteSelected():
            i = 0
            id_list = []

            # loops through the entries in the treetable that have been selected by the user
            while i < len(treetable.selection()):
                selected_item = treetable.selection()[i]
                selected_id = treetable.item(selected_item)["values"][0]
                
                # appends the entries onto a list
                id_list.append(selected_id)

                # deletes every expense that is present in that list, by tracking their ID
                cur.execute("DELETE FROM IDExpenses WHERE ID = (?)", [str(selected_id)])
                i += 1
                
            print("Expenses with IDs:", id_list, "have been deleted.")
            c.commit()
            menu()
            popup()

        """
        old button code:

        delete_selected = Button(window, text="Delete Selected Expenses", padx=2, pady=5, command=lambda: deleteSelected())
        delete_all = Button(window, text="Delete All Expenses", padx=2, pady=5, command=lambda: clearTable())
        
        delete_selected.place(x=400, y=350)
        delete_all.place(x=414, y=390)
        """

        button_temp("Delete Selected\nExpenses", lambda: deleteSelected(), 10, charcoal, 3, 17, 400, 350)
        button_temp("Delete All Expenses", lambda: clearTable(), 10, charcoal, 2, 17, 400, 410)

        menuButton()

    # expense viewing menu
    elif scene == 3:
        # sets various values to filter, then refreshes the table data.
        def newest():
            global filter
            filter = 1
            print("filter updated.")
            table_refresh()

        def oldest():
            global filter 
            filter = 2
            print("filter updated.")
            table_refresh()

        def id_desc():
            global filter 
            filter = 3
            print("filter updated.")
            table_refresh()

        def id_asc():
            global filter 
            filter = 4
            print("filter updated.")
            table_refresh()

        def value_lowest():
            global filter
            filter = 5
            print("filter updated")
            table_refresh()

        def value_highest():
            global filter
            filter = 6
            print("filter updated")
            table_refresh()

        # similar to the menu function, refreshes the table and displays new data, depending on the value of the filter variable.
        def table_refresh():
            for widget in window.winfo_children():
                widget.destroy()

            # background()

            # i = 1
            # for expenses in cur.execute("SELECT * FROM IDExpenses LIMIT 0, 10"):
                # for j in range(len(expenses)):
                    # e = Entry(window, width=15, fg="black")
                    # e.grid(row=i, column=j, pady=2)
                    # e.insert(END, expenses[j])
                # i += 1
            columns = ("ID, Name, Value, Purpose, Date")
            treetable = ttk.Treeview(window, height = 15, show="headings", column=columns)
            
            treetable.heading("#1", text="ID")
            treetable.heading("#2", text="Name")
            treetable.heading("#3", text="Value")
            treetable.heading("#4", text="Purpose")
            treetable.heading("#5", text="Date")

            treetable.column("#1", width=160)
            treetable.column("#2", width=160)
            treetable.column("#3", width=160)
            treetable.column("#4", width=160)
            treetable.column("#5", width=160)

            # default menu
            if filter == 0:
                cur.execute("SELECT * FROM IDExpenses LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)
                
                treetable.place(x=80, y=5)    
                print("Table successfully displayed.")

            # sorts by most recent expense first using the ORDER BY... DESC attributes
            elif filter == 1:
                cur.execute("SELECT * FROM IDExpenses ORDER BY Date DESC LIMIT 0, 15")
                expenses = cur.fetchall()

                # re-inserts the entries in a different, sorted order.
                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)
                print("Table sorted by Date - Newest.") 

            # sorts by oldest expense first
            elif filter == 2:
                cur.execute("SELECT * FROM IDExpenses ORDER BY Date ASC LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)
                print("Table sorted by Date - Oldest.")  

            # sorts by highest ID
            elif filter == 3:
                cur.execute("SELECT * FROM IDExpenses ORDER BY ID DESC LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)
                print("Table sorted by ID - Highest.")                  

            # sorts by lowest ID (default)
            elif filter == 4:                     
                cur.execute("SELECT * FROM IDExpenses ORDER BY ID ASC LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)
                print("Table sorted by ID - Lowest.")

            # sorts by lowest value first
            elif filter == 5:                     
                cur.execute("SELECT * FROM IDExpenses ORDER BY Value ASC LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)
                print("Table sorted by Value - Lowest.") 

            # sorts by highest value first
            elif filter == 6:                     
                cur.execute("SELECT * FROM IDExpenses ORDER BY Value DESC LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)
                print("Table sorted by ID - Highest.")                 
            
            # button_temp("Analyze Expenses", lambda: analyzeExpenses(), 14, charcoal, 2, 15, 54, 290)
            # text, function, fontsize, fontcolor, height, width, xcoord, ycoord

            # sets a coordinate value to make changing the position of each button easier, as the x coordinate of all the buttons are now linked together.
            initside = 50
            
            button_temp("Sort by\nDate - Newest", lambda: newest(), 10, charcoal, 3, 15, initside, 350)
            button_temp("Sort by\nDate - Oldest", lambda: oldest(), 10, charcoal, 3, 15, initside + 145, 350)
            button_temp("Sort by\nID - Highest", lambda: id_desc(), 10, charcoal, 3, 15, initside + 290, 350)
            button_temp("Sort by\nID - Lowest", lambda: id_asc(), 10, charcoal, 3, 15, initside + 435, 350)
            button_temp("Sort by\nValue - Lowest", lambda: value_lowest(), 10, charcoal, 3, 15, initside + 580, 350)
            button_temp("Sort by\nValue- Highest", lambda: value_highest(), 10, charcoal, 3, 15, initside + 725, 350)

            """
            old button filter code:

            newButton = Button(window, text="Sort by Date - Newest", padx=2, pady=5, command=lambda: newest())
            newButton.place(x=initside, y=350)
 
            oldButton = Button(window, text="Sort by Date - Oldest", padx=2, pady=5, command=lambda: oldest())
            oldButton.place(x=initside + 145, y=350)
            
            idHighButton = Button(window, text="Sort by ID - Highest", padx=2, pady=5, command=lambda: id_desc())
            idHighButton.place(x=initside + 290, y=350)

            idLowButton = Button(window, text="Sort by ID - Lowest", padx=2, pady=5, command=lambda: id_asc())
            idLowButton.place(x=initside + 430, y=350)

            valueLowButton = Button(window, text="Sort by Value - Lowest", padx=2, pady=5, command=lambda: value_lowest())
            valueLowButton.place(x=initside + 567, y=350)

            valueHighButton = Button(window, text="Sort by Value - Highest", padx=2, pady=5, command=lambda: value_highest())
            valueHighButton.place(x=initside + 722, y=350)
            """

            menuButton()

        table_refresh()

    # analyze expenses menu
    elif scene == 4:
        today = date.today()
        print(today)

        # calculates the average value after looping through every entry in the table
        def average_value(values):
            value_list = []
            for value in values:
                value_list.append(float(value[1]))

            if len(value_list) == 0:
                print("There are no entries within this timeframe.")
            else:
                print(value_list)
                mean_expense = statistics.mean(value_list)
                print(mean_expense)
                average_expenses = Label(window, text="Average Expenses For This Time Period: " + str(mean_expense))
                average_expenses.pack()


        # returns the sum of every expense after looping through every entry in the table
        def total_value(values):
            total_value = 0
            for value in values:
                total_value += float(value[1])

            print(total_value)
            total_expenses = Label(window, text="Total Expenses For This Time Period: " + str(total_value))
            total_expenses.pack()


        # returns the total and average values of each category.

        def category_analysis():
            global flag
            global entry_break
            if analyze == 5:
                category_y = 340
            else:
                category_y = 380

            # 1 week
            if analyze == 1:
                timespan = today - timedelta(weeks=1)
                cur.execute("SELECT Purpose FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # 1 month (30 days)
            elif analyze == 2:
                timespan = today - timedelta(days=30)
                cur.execute("SELECT Purpose FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # 1 quarter (3 months or 91 days)
            elif analyze == 3:
                timespan = today - timedelta(days=91)
                cur.execute("SELECT Purpose FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # 1 year (365 days)
            elif analyze == 4:
                timespan = today - timedelta(days=365)
                cur.execute("SELECT Purpose FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # all time
            elif analyze == 5:
                cur.execute("SELECT Purpose FROM IDExpenses LIMIT 0, 15")

            selected_categories = []
            for x in cur.fetchall():
                selected_categories.append(x[0])
            print(selected_categories)

            # 1 week
            if analyze == 1:
                timespan = today - timedelta(weeks=1)
                cur.execute("SELECT Value FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # 1 month (30 days)
            elif analyze == 2:
                timespan = today - timedelta(days=30)
                cur.execute("SELECT Value FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # 1 quarter (3 months or 91 days)
            elif analyze == 3:
                timespan = today - timedelta(days=91)
                cur.execute("SELECT Value FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # 1 year (365 days)
            elif analyze == 4:
                timespan = today - timedelta(days=365)
                cur.execute("SELECT Value FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (timespan, today))

            # all time
            elif analyze == 5:
                cur.execute("SELECT Value FROM IDExpenses LIMIT 0, 15")

            selected_values = []
            for x in cur.fetchall():
                selected_values.append(x[0])
            print(selected_values)

            selected_pairs = list(zip(selected_categories, selected_values))
            print(selected_pairs)

            purposes = ["Miscellaneous", "Rent", "Dining", "Clothing", "Entertainment", "Technology", "Utilities", "Groceries", "Loans"]

            def category_stats(category):
                global flag
                global entry_break
                category_sum = []
                non_match = []

                if selected_values == [] or selected_categories == []:
                    no_entries = Label(window, text="There are no entries present.")
                    no_entries.pack()
                    entry_break = 1
                else:
                    if category in selected_categories:
                        for y in selected_pairs:
                            if y[0] == category:
                                category_sum.append(y[1])

                        print(category_sum)

                        category_total = Label(window, text=f"You have spent {sum(category_sum)} on {category}.")
                        category_avg = Label(window, text=f"You have spent an average of {statistics.mean(category_sum)} on {category}.")

                        category_total.place(x=200, y=category_y)   
                        category_avg.place(x=480, y=category_y)  

                        flag = 1
                        print("2", flag)

                    else:
                        flag = 0
                        print("1", flag)

                    print("2.1", flag)
                    entry_break = 0


            for x in purposes:
                #  flag = 0
                print(x)
                category_stats(x)
                print("3", flag)

                if entry_break == 1:
                    break
                    entry_break = 0
            
                if flag == 1:
                    print(category_y)
                    category_y += 20   
                    print("y value incremented.")
                    flag = 0
                else: 
                    print("4", flag)
                    print("No increment here.")

        # these functions change the value of the analyze variable and refresh the menu to display something different
        
        def last_week():
            global analyze
            analyze = 1
            print("Timeframe set to one week ago.")
            analyze_menu()


        def last_month():
            global analyze
            analyze = 2
            print("Timeframe set to one month ago.")
            analyze_menu()


        def last_quarter():
            global analyze
            analyze = 3
            print("Timeframe set to three months ago.")
            analyze_menu()


        def last_year():
            global analyze
            analyze = 4
            print("Timeframe set to 1 year ago.")
            analyze_menu()


        def all_time():
            global analyze
            analyze = 5
            print("Timeframe set to all-time.")
            analyze_menu()

        def monthly_analyze():
            global analyze 
            analyze = 6
            print("Analyzing by month.")
            analyze_menu()


        def timespan_dropdown():
            global analyze

            time_periods = ["One Week Ago", "One Month Ago", "Three Months Ago", "One Year Ago", "All-Time"]

            timespan_width = len(max(time_periods, key = len))
            timespan_tkvar = StringVar(window)
            timespan_tkvar.set(" ")
            timespanMenu = OptionMenu(window, timespan_tkvar, *time_periods)
            timespanMenu.config(width = timespan_width)
            timespanMenu.place(x=168, y=335)


            def get_timespan():
                timespan_info = timespan_tkvar.get()
                print(timespan_info)

                if timespan_info == time_periods[0]:
                    last_week()

                elif timespan_info == time_periods[1]:
                    last_month()

                elif timespan_info == time_periods[2]:
                    last_quarter()
                
                elif timespan_info == time_periods[3]:
                    last_year()
                
                elif timespan_info == time_periods[4]:
                    all_time()


            button_temp("Select\nTimespan", lambda: get_timespan(), 10, charcoal, 2, 10, 80, 335)


        # TODO: write a function similar to timespan_dropdown(), but have it display monthly data going back 1 year ago; change this later to start from 10 years ago and auto-update itself.
        def monthly_dropdown():
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            defaultyear = 2000
            years = []

            while defaultyear <= today.year:
                years.append(defaultyear)
                defaultyear += 1


            print(years)

            monthly_width = len(max(months, key=len))

            monthly_tkvar = StringVar(window)
            monthly_tkvar.set(" ")
            monthlyMenu = OptionMenu(window, monthly_tkvar, *months)
            monthlyMenu.config(width = monthly_width)
            monthlyMenu.place(x=168, y=378)

            yearChoice_tkvar = StringVar(window)
            yearChoice_tkvar.set(" ")
            yearChoiceMenu = OptionMenu(window, yearChoice_tkvar, *years)
            yearChoiceMenu.config(width = 5)
            yearChoiceMenu.place(x=269, y=378)


            def get_monthly():
                monthly_info = monthly_tkvar.get()
                yearChoice_info = yearChoice_tkvar.get()

                month_start = datetime(int(yearChoice_info), int(months.index(monthly_info)) + 1, 1)
                thirty_one_day_months = ["January", "March", "May", "July", "August", "October", "December"]
                thirty_day_months = ["April", "June", "September", "November"]

                if monthly_info in thirty_one_day_months:
                    month_end = datetime(int(yearChoice_info), int(months.index(monthly_info)) + 1, 31)
                
                elif monthly_info in thirty_day_months:
                    month_end = datetime(int(yearChoice_info), int(months.index(monthly_info)) + 1, 30)
                
                elif monthly_info == "February" and int(yearChoice_info) % 4 == 0:                     
                    month_end = datetime(int(yearChoice_info), int(months.index(monthly_info)) + 1, 29)
                
                else:
                    month_end = datetime(int(yearChoice_info), int(months.index(monthly_info)) + 1, 28)

                print(month_start)
                print(month_end)

                for widget in window.winfo_children():
                    widget.destroy()

                columns = ("ID, Name, Value, Purpose, Date")
                treetable = ttk.Treeview(window, height = 15, show="headings", column=columns)
                
                treetable.heading("#1", text="ID")
                treetable.heading("#2", text="Name")
                treetable.heading("#3", text="Value")
                treetable.heading("#4", text="Purpose")
                treetable.heading("#5", text="Date")

                treetable.column("#1", width=160)
                treetable.column("#2", width=160)
                treetable.column("#3", width=160)
                treetable.column("#4", width=160)
                treetable.column("#5", width=160)
                        
                cur.execute("SELECT * FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (month_start, month_end))
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()
                # calculates the average value of each expense and the total expenses for this period of time (in this case, one week)
                average_value(expenses)
                total_value(expenses)
                print("Expenses from 1 week ago have been shown.")

                # displays measures per category
                category_analysis_button()
                timespan_dropdown()
                monthly_dropdown()
                menuButton()

                """
                cur.execute("SELECT * FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (month_start, month_end))
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()

                average_value(expenses)
                total_value(expenses)
                """

            button_temp("Select Month\nTo Analyze", lambda: get_monthly(), 10, charcoal, 2, 10, 80, 378)


        def category_analysis_button():
            button_temp("Analyze By\n Category", lambda: category_analysis(), 14, charcoal, 2, 12, 800, 400)          


        def analyze_menu():
            for widget in window.winfo_children():
                widget.destroy()

            # background()

            columns = ("ID, Name, Value, Purpose, Date")
            treetable = ttk.Treeview(window, height = 15, show="headings", column=columns)
            
            treetable.heading("#1", text="ID")
            treetable.heading("#2", text="Name")
            treetable.heading("#3", text="Value")
            treetable.heading("#4", text="Purpose")
            treetable.heading("#5", text="Date")

            treetable.column("#1", width=160)
            treetable.column("#2", width=160)
            treetable.column("#3", width=160)
            treetable.column("#4", width=160)
            treetable.column("#5", width=160)

            # default menu
            if analyze == 0:
                """
                weekButton = Button(window, text="Analyze From 1 Week Ago", padx=2, pady=5, command=lambda: last_week()) 
                monthButton = Button(window, text="Analyze From 1 Month (30 Days) Ago", padx=2, pady=5, command=lambda: last_month())
                quarterButton = Button(window, text="Analyze From 3 Months Ago", padx=2, pady=5, command=lambda: last_quarter())
                yearButton = Button(window, text="Analyze From 1 Year Ago", padx=2, pady=5, command=lambda: last_year())
                allTimeButton = Button(window, text="Analyze All-Time Results", padx = 2, pady=5, command=lambda: all_time())

                weekButton.pack()
                monthButton.pack()
                quarterButton.pack()
                yearButton.pack()
                allTimeButton.pack()
                """
                cur.execute("SELECT * FROM IDExpenses LIMIT 0, 0")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.place(x=80, y=5)

                timespan_dropdown()
                monthly_dropdown()

            # retrieves entries from exactly one week prior to the current date
            elif analyze == 1:
                oneweekago = today - timedelta(weeks=1)
                cur.execute("SELECT * FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (oneweekago, today))
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()
                # calculates the average value of each expense and the total expenses for this period of time (in this case, one week)
                average_value(expenses)
                total_value(expenses)
                print("Expenses from 1 week ago have been shown.")

                # displays measures per category
                category_analysis_button()

                timespan_dropdown()
                monthly_dropdown()

            # retrieves entries from exactly 30 days prior to the current date
            elif analyze == 2:
                onemonthago = today - timedelta(days=30)
                cur.execute("SELECT * FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (onemonthago, today))
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()
                average_value(expenses)
                total_value(expenses)
                print("Expenses from 1 month ago have been shown.")

                # displays measures per category
                category_analysis_button()

                timespan_dropdown()
                monthly_dropdown()

            # retrieves entries from exactly 91 days (3 months) prior to the current date 
            elif analyze == 3:
                onequarterago = today - timedelta(days=91)
                cur.execute("SELECT * FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (onequarterago, today))
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()
                average_value(expenses)
                total_value(expenses)
                print("Expenses from 1 quarter ago have been shown.")

                # displays measures per category
                category_analysis_button()

                timespan_dropdown()
                monthly_dropdown()

            # retrieves entries from exactly 365 days (1 year) prior to the current date
            elif analyze == 4:
                oneyearago = today - timedelta(days=365)
                cur.execute("SELECT * FROM IDExpenses WHERE Date >= (?) and Date <= (?) LIMIT 0, 15", (oneyearago, today))
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()
                average_value(expenses)
                total_value(expenses)
                print("Expenses from 1 year ago have been shown.")

                # displays measures per category
                category_analysis_button()

                timespan_dropdown()
                monthly_dropdown()

            # displays the total sum and percentage of each category of expense.
            elif analyze == 5:
                cur.execute("SELECT * FROM IDExpenses LIMIT 0, 15")
                expenses = cur.fetchall()

                for row in expenses:
                    treetable.insert("", END, values=row)

                treetable.pack()
                average_value(expenses)
                total_value(expenses)
                print("Expenses from all-time have been shown.")

                category_analysis_button()

                timespan_dropdown()
                monthly_dropdown()

            # back button to return the to first menu
            menuButton()

        # initializes the GUI for the first time this menu is accessed 
        analyze_menu()

# initializes the GUI for the first time this menu is accessed
menu()

# this is used to display widgets onto the screen
window.mainloop()

# closes the connection to the sqlite database; keeping it open is bad.
# we close the connection at the end of the script instead of after each c.commit() because the data has to constantly be accessed, and repeatedly 
# closing and opening the connection throws up errors, and this was the most efficient way i found to do it.
c.close()
# make sure you add c.close somewhere to close the connection afterwards