# Introduction
This is a coding challenge which I practiced for improving my data engineering skills. The original Challenge summary and requirements can be found at [InsightDataScience/donation-analytics](https://github.com/InsightDataScience/donation-analytics).

# Input File 
1. itcont.txt

   From each record, below information should be extracted:
   
   CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution
   
   NAME: name of the donor

   ZIP_CODE: zip code of the contributor (we only want the first five digits/characters)
   
   TRANSACTION_DT: date of the transaction
   
   TRANSACTION_AMT: amount of the transaction
   
   OTHER_ID: a field that denotes whether contribution came from a person or an entity

2. pertentile.txt

   This file holds a single value -- the percentile value (1-100) that your program will be asked to calculate. 

# Step
## 1. Import Data and Filter Invalied records
Read the whole file as a pandas DataFrame and rename the needed columns by refering to the data dictionary [as described by the FEC.](https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml)

Select the needed columns and drop records if:
   If OTHER_ID contains any other value than NaN
   If TRANSACTION_DT is an invalid date (e.g., empty, malformed)
   If ZIP_CODE is an invalid zip code (i.e., empty, fewer than five digits)
   If the NAME is an invalid name (e.g., empty, malformed)
   If any lines in the input file contains empty cells in the CMTE_ID or TRANSACTION_AMT fields

Format the DataFrame:
   For column ZIP_CODE: get the first five digits
   Add a new column YEAR, extracting the last four digits from TRANSACTION_DT
   Add a new column DONOR_ID and the value is a tuple of (NAME,ZIP_CODE)  

## 2. Identifying repeat donors
Group the DataFrame by DONOR_ID, and calculate in how many years has a DONOR_ID made a donation by using .nunique().
If a DONOR_ID contributed in more than one year, this DONOR_ID is a repeat donor.
Select all the records for repeat donors and create a list of dictionaries in which each dictionary contains a record.


## 3. Calculations
For each record, make a new tuple of (recipient, zip code and calendar year), calculate these three values for contributions coming from repeat donors:
   total dollars received
   total number of contributions received
   donation amount in a given percentile P 

# Requirements
`pip install numpy pandas`

# How to run
1. Please put itcoin.txt and pertencile.txt in the input folder
2. run

   `$ ./run.sh`

3. The output file repeat_donor.txt will be created in the output folder

