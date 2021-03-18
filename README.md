# Options Decision Support System (ODSS)

## Introduction

ODSS is a decision support tool that assist the user in identifying profitable optios trades given their portfolio and valuation preferences

This tool assumes that you have experience with options trading and can benefit from technological assistance in your market analysis.

This tool is not "magic" and does not replace having your own strategy and knowledge. 

In fact, to date, this tool is developed to satisfy 1 user, me! Current features are optomized for my most common strategy, which is somewhat idiosyncratic. However, expanding features for more general uses is happening now, and input and participation are welcome.

## Project

Current functionality is limited to showing the results of running a simple contract picking algorithm against a provided portfolio

Near future functionality will facilitate ad-hoc exploration of the options market, modifying algorithm parameters, selection of addiitonal algorithms, and saving of program state and stock data

Far future functionality will include graphical user interface and API linkages to user brokerage for automated portfolio modeling

## Usage
    
The simplest way to use the program is to type "python main.py" from the top program directory. This will execute the program. If you want to just see it in action, you can hit enter at each prompt. This will select default options, which will run through the offline demo and then exit.
    
You may select alterate options at each prompt. For example, loading a custom portfolio or choosing a different algorithm (only one is implmented at the moment.) Note, if you select a portfolio besides the demo one, the program will always look for pricing data online. So it is recommended to do this during market hours.

Notably, the application requires the user to identify securities of interest, their valuation of the security (in the form of buy and sell prices) and an algorithm to follow for exploring the option contract space and selecting trades of interest. These are critical responsibilities and it is important to understand how the algorithm performs around them. That said, accomplishing this should greatly reduce the time spent per trade and imporve the chance of discovering arbitrage and high value opportunities.

The program will display the output of the selected algorithm (currently, this will be a list of selected contracts by the naive_best_daily approach) and then await further user input.

### Portfolio file format

A user portfolio file is an important piece of input for using the program. Future version may abstract this into a program state file and support features such as pulling data from accounting and brokerage applications, but presently the user should build their own .csv file in the below format:

variable | type  | decsription
---------|-------|---------------------
ticker   | a...z | ticker symbol of security of interest, or "cashposition"
shares   | int   | number of shares held in position. 0 is acceptable
buy      | float | the most one is willing to pay for a share today
sell     | float | the least one is willing to sell a share for today

furthermore, one of the ticker symbols cam be labeled "cashposition" and include your current cash available in the "shares" column. The buy and sell entries will be ignored for that row. If absent, the application will assume 0 cash.

### Algorithms

Like the portfolio, algorithm selection is an important user responsibility. The format and content of the program's output is dependent on algorithm selection. Currently one algorithm is available, and its parameters are fixed. 

#### naive_best_daily

the naive best daily algorithm aims to identify which options contracts to sell to earn the most money per day in the portfolio. It limits its exploration of the contract space to calls with strike prices at or above the users minimum sell price, and put contract with strikes at or below the user's buy price. Furthermore, an annual appreciation-inflation discount is applied that penalizes these boundaries by 20% per year. Earnings per day are calculated from the current date to contract expiration. In the case of put writes, this valuation is further adjusted by the cash outlay (strike price times 100) necessary for the position, and contracts ranked by this daily income per dollar out, instead of simple daily income.

Final selections provided to the user include the highest performing call option for each security in the portfolio, plus the highest performing put options up the the user's cash limit (so if they sold as many contracts as affordable in the highest earning put, then as many as affordable with the remaining capital in the next security, and so on.) 

These results are presented to the 

It is possible for no trades to match the user's parameters, in which case a blank table is provided.

Note, the final selections of the naive_best_daily do not assume diversitication, but instead concentration of position. It is also currently designed to limit, rather than expand, one's understanding of the options space and near, but not selected, contracts. 

## Provided files

The core program exist as three files containing two classes and a user interface. These are:

./main.py - the user interface. start here if curious to try it out

./portfolio.py - contains the portfolio class, which executes portfolio level calculations and generates stock classes

./stock_option.py - contains the stock_option class, currently contains the nuts and bolts of algorithms and data querrying. Look here if wanting to review these key features

Demo data are available in the ./data subdirectory

./data/sample_portfolio.csv - contains a sample portfolio for use with the provided demo

./data/[ticker].csv - there are 4 csv files each named with a stock ticker. These can be used with demo mode if not wantign to pull data from internet

If you are missing files, or they are not in the correct directories, the program may not work. Please ensure the files are available.

## Testing and Caveats
    
A test script is available at test.py. This is used to make sure the stock option class is performing correctly. test.py should run to end without errors. Two of the data quality tests require the user to observe data frames contained within the stock object. These data frames are printed for the user to observe data quality qualitatively.

Note, a lot could still go wrong. In particular, connectivity issues are not addressed in the current build. Furthermore, variations in information presentation and availability from the primary data source (yahoo finance) may present hereto unknown errors. 

Please report any errors, and, if known, possible fixes, to me for future revision.
    
## Participating
    
If this project is interesting to you, feel free to reach out to the creator:
    
Ronald Buie 

[lastname]rw [at] uw + edu
        
The git for the non course version can be found at:

https://github.com/rwbuie/ODSS