# Dividend Analyzer TBD

The idea for the project stems from the lack of a valid and convenient tool for analysing the dividends of Italian companies listed on the Italian Stock Exchange, in particular those belonging to the FTSE All Share index.

The goal is to analyse a list of dividend-paying companies in order to choose the best, most profitable ones on the basis of certain parameters such as dividend yield or yield ratio.

## Description

The project essentially contains four main scripts:
- companies_downloader_from_milanofinanza.py: script downloading all companies by extracting data from the site milanofinanza.it and create a file to store them.
- companies_downloader_from_sole24ore.py: script downloading all companies by extracting data from the site ilsole24ore.it and create a file to store them.
- data_downloader.py: a script that downloads data from Yahoo Finance via the yfinance library (https://github.com/ranaroussi/yfinance), storing them in .csv files in the dataset folder and creating a convenience file containing the most useful information for each company;
- analyzer.py: script that analyses the previously stored files, producing an analysis file in .csv and .xslx format as output

The companies that will be analysed are contained in the companies.csv file. Edit this file to have different companies analysed.

The companies are ordered according to the following parameters:
- **yieldRatio**: descending order, it is the ratio of the number of years in which the dividend is detached over the number of years of analysis; 
- **yearTimePeriod**: descending order, it is the number of years analysed for that company;
- **dividendYield**: descending order, the ratio of the value of the ex-dividend to the share price the day before, representing the efficiency of the dividend;
- **currentPrice**: ascending order, the share price in its current state; this parameter is of interest because it is the price you have to pay to own the stock in order to receive the dividend.

## Getting Started

### Installing

* Install Python moduls nedeed

```
pip install -r requirements.txt
```

### Executing program

* Run companies downloader script

You can choose different platforms from which download companies data:
- Milano Finanza
- Il Sole 24 Ore

 Based on that, you can run the proper script, which will produce a file .csv called *companies.csv*:
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
