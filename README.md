# Dividend Analyzer

The idea for the project stems from the lack of a valid and convenient tool for analysing the dividends of Italian companies listed on the Italian Stock Exchange, in particular those belonging to the FTSE All Share index.

The goal is to analyse a list of dividend-paying companies in order to choose the best, most profitable ones on the basis of certain parameters such as dividend yield or yield ratio.

## Description

The project essentially contains main scripts:
- companies_downloader_from_borsaitaliana.py: script downloading all companies by extracting data from the site borsaitaliana.it and create a file to store them.
- companies_downloader_from_milanofinanza.py: script downloading all companies by extracting data from the site milanofinanza.it and create a file to store them.
- companies_downloader_from_sole24ore.py: script downloading all companies by extracting data from the site ilsole24ore.it and create a file to store them.
- data_downloader_multithread.py: a script that downloads data from Yahoo Finance via the yfinance library (https://github.com/ranaroussi/yfinance), storing them in .csv files in the dataset folder and creating a convenience file containing the most useful information for each company;
- analyzer.py: script that analyses the previously stored files, producing an analysis file in .csv and .xslx format as output

The companies that will be analysed are contained in the companies.csv file. Edit this file to have different companies analysed.

The companies are ordered according to the following parameters:
- **yieldRatio**: descending order, it is the ratio of the number of years in which the dividend is detached over the number of years of analysis; 
- **yearTimePeriod**: descending order, it is the number of years analysed for that company;
- **dividendYield**: descending order, expressed as percentage, is the ratio of the value of the ex-dividend to the share price the day before, representing the efficiency of the dividend;
- **currentPrice**: ascending order, the share price in its current state; this parameter is of interest because it is the price you have to pay to own the stock in order to receive the dividend.

Other information about fields:
- **dividentRate**: are expressed as an actual dollar amount and not a percentage, which is the amount per share that an investor receives when the dividend is paid. The rate may be either fixed or adjustable, depending on the company.
 Here’s an example: Let’s assume that Company X’s stock pays an annual dividend of $4 per share in four quarterly payments. So for each payment, an investor receives a dividend of $1. The dividend rates are $1 per quarter and $4 annually. Quarterly dividends are the most common for U.S.-based dividend-paying companies. However, some companies will distribute dividends annually, semiannually, or even monthly.
- **longestYieldStrike**: is the longest strike of consecutive dividends paid.
- **yearTimePeriod**: duration as number of year from which we have data available.
- **yieldCounter**: how many dividend paid during yearTimePeriod.
- **firstDividendDate**: first date available where dividend was paid.
- **lastDividendDate**: last date available where dividend was paid (except current year).
- **lastDividendValue**: value of last dividend paid.
- **lastPriceWithDividend**: last price of stock when last dividend was paid.
- **minDivided**: minimum dividend paid.
- **maxDivided**: maximum dividend paid.
- **avgDivided**: average dividend paid.
- **stdDivided**: standard deviation of dividend paid.
- **currency**: currency of the dividend and the price.

**P.S. dividend with release date lower than year 2002 (€ begining date...) are converted from Lira italiana to €.**

### Final considerations
Based on fields (yieldRatio, yearTimePeriod, dividendYield, currentPrice) you should prefer the companies:
1) With the highest yieldRatio first because represent the 'reliabiliy' in paying divideds.
2) With the longest time period, because 30 years of dividends are more reliable than 2 years :)
3) With the highest dividendYield, representing the dividend efficiency ( as ratio between dividend value and the stock price).
4) Last, with the lowest stock price, because you have to pay as less as possible to get a certain amount of dividend.
    E.g. with dividendYield = 5 %, you should prefer a stock pricing 5€ instead of 100€ because you can get more stocks paying less.

## Getting Started

### Installing

* Install Python modules nedeed

```
pip install -r requirements.txt
```

### Executing program

* Run companies downloader script

You can choose different platforms from which download companies data:
- Borsa Italiana
- Milano Finanza
- Il Sole 24 Ore

Based on that, you can run the proper script, which will produce a file .csv called *companies.csv*:
```
python companies_downloader_from_borsaitaliana.py
```
```
python companies_downloader_from_sole24ore.py
```
```
python companies_downloader_from_milanofinanza.py
```
* Run downloader script
 
```
python data_downloader.py
```
* Run the analyzer script
 
```
python analyzer.py
```

At the end of the script execution, the analysis file produced will be located in the output folder.

## Authors

Francesco Miliani
[@francescomiliani18] (https://www.linkedin.com/in/francescomiliani18/)

## Version History

* 0.4
    * Add borsa italiana companies downloaders
    * See [commit change]() or See [release history]()
      
* 0.3
    * Add companies downloaders
    * See [commit change]() or See [release history]()
      
* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
