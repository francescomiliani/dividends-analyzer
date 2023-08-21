# Dividend Analyzer TBD

The idea of the project is to analyse a list of dividend-paying companies in order to choose the best, most profitable ones on the basis of certain parameters such as dividend yield or yield ratio.
## Description

The project essentially contains two main scripts:
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

* Install Python 3 from the official site: https://www.python.org/downloads/
* Install Pandas library

```
pip install pandas
```

### Executing program

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

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
