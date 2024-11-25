# Name: Raluca Ciobanu
# Student Number: c00289426
# Date: November 2024.
# run.py is an entry point of entry for any server wishing to run this app.

from app import app

# The if __name__ == '__main__': block ensures that the app.run() method is only 
# called if the script is run directly, and not if it is imported as a module.
if __name__ == "__main__":
    app.run()