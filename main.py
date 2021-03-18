from portfolio import portfolio as port
from os import path
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)


def demo_option():
    """
    prompts user if they wish to use demo data
    loop continues until user enters y or n
    <enter> defaults to n
    returns boolean
    """
    demo = 2
    while demo == 2:
        print("Do you want to retrieve live data? If not, \
            demo data will be used.")
        print("If outside of market hours, demo data are suggested.")
        choice = input("y/N: ")
        if choice.lower() == "n" or choice == "":
            demo = True
        elif choice.lower() == "y":
            demo = False
        else:
            print("invalid selection. Please try again.")
    return(demo)


def find_file():
    """
    prompts user for portfolio file
    loop continues until a file is identified
    <enter> defaults to provided sample
    returns file path
    """
    located = False
    while not located:
        file = input("Enter location of portfolio or "
                     "<enter> for default sample: ")
        if file == "":
            file = "./data/sample_portfolio.csv"
            located = True
        else:
            if path.exists(file):
                located = True
            else:
                print("error, file not found at " + file)
                print("please try again")
    print("portfolio found.")
    return(file)


def main():
    """
    provides interactive interface for options decision support tool
    if selecting defaults, will look for files in ./data
    see README.md for details
    """
    print("#################################################################")
    print("Welcome to Ron's ODSS (Options Decision Support System)")
    print("This tool helps identify the most profitable options to sell")
    print("This is a prototype developed for a python course")
    print("For the latest version and other help, pleaes see README.md")
    print("And remember, stonks go up")
    print("#################################################################")
    continue_primary_loop = True
    file = ""
    while continue_primary_loop:
        if file == "":
            file = find_file()
        else:
            exit_loop = False
            while not exit_loop:
                print(file + " already selected")
                choice = input("Do you want to change it? y/N: ")
                if choice.lower() == "y":
                    file = find_file()
                    exit_loop = True
                elif choice.lower() == "n" or choice == "":
                    exit_loop = True
                    print()
                else:
                    print("invalid input")
                    print()

        if file == "./data/sample_portfolio.csv":
            demo = demo_option()
        else:
            demo = False

        strategy = ""
        while strategy == "":
            print("please select one of the following strategies")
            print("(1) naive best daily income (default)")
            choice = input("select: ")
            if choice == "1" or choice == "":
                strategy = "naive_best_daily"
            else:
                print("Invalid selection. Please try again.")

        print()
        print()

        stocks = port(file, demo, strategy)

        print()
        print()
        print("optimum trades identified using " + stocks.current_strategy())
        print()
        df = stocks.report_trades()
        print(df.to_string(index=False))
        print()

        continue_sub_loop = True
        while continue_sub_loop:
            choice = "x"
            print("MENU")
            print("(1) Try Again")
            print("e(X)it <default>")
            print()
            choice = input("select:")
            print()
            if choice == "1":
                continue_sub_loop = False
            elif choice.lower() == "x" or choice == "":
                continue_sub_loop = False
                continue_primary_loop = False
            else:
                print("invalid choice")
                print()


if __name__ == '__main__':
    main()
