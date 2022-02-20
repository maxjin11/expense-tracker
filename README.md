# Personal Finance Manager - by Max Jin

This is a program used to keep track of various expenses made by the user.
This program was written using Python 3.
This project was started during June 2021.

CURRENT FEATURES:
- Uses an sqlite database to keep track of expenses
  - These expenses can be added or deleted
  - Each expense entry contains a name, a unique id to the database, the cost, a category, and a date.
- The GUI is designed with the Tkinter package
  - Presents expenses in a clean, visible table
  - Adding, deleting, viewing, and analytical functions straightforward to use
- Analytical functions:
  - Filters expenses by various time periods:
    - Any given month of years dating from 2000
    - One week ago, one month ago, three months ago, or one year ago, or all-time

PLANNED FEATURES:
- Feature which exports select expenses to a neatly formatted Excel spreadsheet
- More dropdown selection for various features, less buttons
- Monthly expense comparisons
- Bar graphs for month-month comparisons, pie charts for category comparisons
