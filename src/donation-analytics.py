import sys
import pandas as pd
import numpy as np
import math

#read input file as a pandas datafram and rename columns
#column 10 is zipcode, need to convert to str
raw_data = pd.read_csv(sys.argv[1], sep="|", header=None, dtype={10:str})
raw_data.rename(columns={0:'CMTE_ID'}, inplace=True)
raw_data.rename(columns={7:'NAME'}, inplace=True)
raw_data.rename(columns={10:'ZIP_CODE'}, inplace=True)
raw_data.rename(columns={13:'TRANSACTION_DT'}, inplace=True)
raw_data.rename(columns={14:'TRANSACTION_AMT'}, inplace=True)
raw_data.rename(columns={15:'OTHER_ID'}, inplace=True)

#data validation: delete unvalid data records
selected_data = raw_data[['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']].copy()
selected_data = selected_data.dropna(subset=['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT'])
selected_data = selected_data[pd.isnull(selected_data['OTHER_ID'])]
#edit zipcode
selected_data = selected_data[selected_data['ZIP_CODE'].apply(lambda x:len(x)>=5)]
selected_data['ZIP_CODE'] = selected_data['ZIP_CODE'].apply(lambda x:x[:5])
#get the year of the record
selected_data['YEAR'] = selected_data['TRANSACTION_DT'].apply(lambda x : int(str(x)[-4:]))
#identify unique donor by make NAME and Zipcode a tuple, name it 'Donor ID'
selected_data['DONOR_ID'] = selected_data[['NAME', 'ZIP_CODE']].apply(tuple, axis=1)
#delete useless columns
selected_data = selected_data.drop(['OTHER_ID','NAME','TRANSACTION_DT'],axis = 1)

#find repeat donor

#find out for each donor, for how many years has this donor contributed?
contributed_year_count = selected_data.groupby('DONOR_ID')['YEAR'].nunique()
#if the count > 1, the donor is a repeated donor
repeat_donor = contributed_year_count[contributed_year_count>1].index.values
#get a cleaned dataset with only repeat donor records, by referencing the donor list got from repeat_donor
repeat_donor_data = selected_data.loc[selected_data['DONOR_ID'].isin(repeat_donor)].copy()

#make each record a dictionary and put it in a list
repeat_donor_data_list = repeat_donor_data.to_dict('records') #list of dictionary
#print(repeat_donor_data_list)

#calculate

#read P from percentile.txt
percentile_file = open(sys.argv[2])
P = int(percentile_file.read())
datadict = {}
firstyeardict = {}
amount_list = []
output_file = open(sys.argv[3],'a')
for i in repeat_donor_data_list:
    if i['DONOR_ID'] not in firstyeardict:
        firstyeardict[i['DONOR_ID']] =i['YEAR']
    elif i['YEAR'] != firstyeardict[i['DONOR_ID']]:
        key = (i['CMTE_ID'],i['ZIP_CODE'],i['YEAR'])
        count = 1
        value = [i['TRANSACTION_AMT'],count]
        if key not in datadict:
            datadict[key] = value
            amount_list.append(i['TRANSACTION_AMT'])
            index = (math.ceil((P/100)*datadict[key][1]))-1
        else:
            datadict[key][0] = datadict[key][0] + i['TRANSACTION_AMT']
            datadict[key][1] = datadict[key][1] + 1
            amount_list.append(i['TRANSACTION_AMT'])
            index = (math.ceil((P/100)*datadict[key][1]))-1
        amount_list.sort()
        output_list = [i['CMTE_ID'],i['ZIP_CODE'],i['YEAR'],amount_list[index],datadict[key][0],datadict[key][1]]
        output_str = '|'.join(map(str,output_list))
        print(output_str)
        output_file.write(output_str+'\n')
output_file.close()