# Data Pre-processing and Data Set Generation

Data set generation steps:

1. Run dataConversion.py to create data sets for Germany, Italy and the US from source data in ./source-data/ (version: 14.07.2020): covid-ger.csv, covid-it.csv, covid-us.csv
2. Now manually integrate the summary data from ./source-data/Summary_stats_Germany.csv for data augmentation into covid-ger.csv: covid-ger-extended.csv
3. Remove all rows from a copy of the csv files which include NaN values in order to make them compatible with existing methods: covid-ger-extended-trim.csv, covid-it-trim.csv, covid-us-trim.csv  