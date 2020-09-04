need to install anaconda 3
need to install matching version of selenium driver for chrome


how to use:

in the root directoy, create a csv file called asin.csv
--- format should be like this below..
ASIN
1133307434
0134639715
8185787123
1133958095
1435462858

then set the settings..

numOfLists = 2  # will create x number of lists -- more efficient so you can run multiple processes in parallel
startNum = 0
recordsPerList = 2 # nukmber of records that go in each list defined in numOfLists


--- it should create csv files that stores each list...
--- there should be a combined list at the end called combinedCSV.csv