import pandas as pd
import sys 
import os
#sys.path.append(os.path.abspath("C:\\Users\\lexfo\\Documents\\studeren\\Master_JADS\\thesis\\Code_for_BOT\\current_container\\Python_financial_container\\thesis_code"))
from LJT_database.make_query import *
from LJT_helper_functions.helpers import *
from datetime import datetime 
list_not_to_merge = ['econ_bitcoin', 'events_crypto']

def rename_columns(dataframe, coinpair, table):
    columns = list(dataframe.columns)
    new_columns = ['last_start_time']
    new_columns.extend(f"{coinpair}__{table}__{column}" for column in columns[1:])
    new_names = {columns[j]: new_columns[j] for j in range(len(columns))}
    return dataframe.rename(columns=new_names)

def merge_all_tables_in_dataset(coinpair, dict_with_structure):
    if coinpair in dict_with_structure.keys():
        all_tables_in_coinpair_dataset = dict_with_structure[coinpair]
        final_dataframe_coinpair = extract_dataset(coinpair, all_tables_in_coinpair_dataset[0],1581012000000.0) #create a dataframe from the first table in coinpair dataset to further merge with other tables
        final_dataframe_coinpair_unique = final_dataframe_coinpair.drop_duplicates(['last_start_time'])
        final_dataframe_coinpair_unique = rename_columns(final_dataframe_coinpair_unique, coinpair,all_tables_in_coinpair_dataset[0])

        for i in range(1, len(all_tables_in_coinpair_dataset)):
            print(all_tables_in_coinpair_dataset[i])
            dataframe = extract_dataset(coinpair, all_tables_in_coinpair_dataset[i],1581012000000.0)
            dataframe_unique = dataframe.drop_duplicates(['last_start_time'])
            dataframe_unique = rename_columns(dataframe_unique, coinpair, all_tables_in_coinpair_dataset[i])
            final_dataframe_coinpair_unique = pd.merge(final_dataframe_coinpair_unique, dataframe_unique, on='last_start_time',how='outer')
        print(' ---> Done', dict_with_structure[coinpair], 'are merged')

        final_dataframe_unique = final_dataframe_coinpair_unique.drop_duplicates(['last_start_time'])
        return final_dataframe_unique
    else:
        print('the coinpair cannot be found in Google BQ')

def merge_split_coins(coinpair, dict_with_structure):
    key, target = split_all_coinpairs(coinpair)
    print('Now', key.upper(), 'and', target.upper(), 'are merged')

    if len(dict_with_structure[key.upper()]) == 1 and len(dict_with_structure[target.upper()]) == 1:
        dataframe_of_key = extract_dataset(key.upper(), dict_with_structure[key.upper()][0],1581012000000.0)
        dataframe_of_key_unique = dataframe_of_key.drop_duplicates(['last_start_time'])
        dataframe_of_key_unique = rename_columns(dataframe_of_key_unique, key.upper(),dict_with_structure[key.upper()][0])
        dataframe_of_target = extract_dataset(target.upper(), dict_with_structure[target.upper()][0],1581012000000.0)
        dataframe_of_target_unique = dataframe_of_target.drop_duplicates(['last_start_time'])
        dataframe_of_target_unique = rename_columns(dataframe_of_target_unique, target.upper(),dict_with_structure[target.upper()][0])

        final_dataset_individual_coins = pd.merge(dataframe_of_key_unique, dataframe_of_target_unique,on='last_start_time',how='outer')
        print('---> Done', key.upper(), target.upper(), 'are merged')
        final_dataset_individual_coins_unique = final_dataset_individual_coins.drop_duplicates(['last_start_time'])
        return final_dataset_individual_coins_unique
    else:
        print('.... Merging tables of', key.upper())
        final_dataset_key = merge_all_tables_in_dataset(key.upper(), dict_with_structure)
        print('.... Merging tables of', target.upper())
        final_dataset_target = merge_all_tables_in_dataset(target.upper(), dict_with_structure)
        final_dataset_individual_coins = pd.merge(final_dataset_key, final_dataset_target, on='last_start_time')
        print(key.upper(), 'and', target.upper(), 'are succesfully merged')
        return final_dataset_individual_coins

def merge_remaining_tables(dict_with_structure):
    print('Now general_info is merged')
    final_dataset_general_info = merge_all_tables_in_dataset('general_info', dict_with_structure)
    return final_dataset_general_info

def final_merger(coinpair):
    print('Merging process started')
    print('')
    dict_with_structure = return_dataset_names(list_not_to_merge)
    print('The structure on Google Bigquery look as follows:')
    for i in dict_with_structure.items():
        print(i)
    print('')
    print('First the tables in', coinpair, 'dataset are merged:')
    final_dataset_per_coinpair = merge_all_tables_in_dataset(coinpair, dict_with_structure)
    print('')
    print(len(final_dataset_per_coinpair))
    final_dataset_individual_coins = merge_split_coins(coinpair, dict_with_structure)
    print('')
    print(len(final_dataset_individual_coins))
    final_dataset_general_info = merge_remaining_tables(dict_with_structure)
    print(len(final_dataset_general_info))
    print('')
    print('Finally merge all these datasets together:')
    semi_total_dataset = pd.merge(final_dataset_per_coinpair, final_dataset_individual_coins, on='last_start_time')
    total_dataset = pd.merge(semi_total_dataset, final_dataset_general_info, on='last_start_time')
    print('---> Done, all tables are succesfully merged!')
    day = datetime.today()
    total_dataset = total_dataset.sort_values('last_start_time', ascending=True)
    total_dataset.to_csv(f'data/totale_dataset_{day.day}_{day.month}_{coinpair}.csv', index = False)
    print('dataset stored')
    
    return total_dataset
