import pandas as pd
import glob
from datetime import datetime

def get_csv_files(path_pattern):
    return glob.glob(path_pattern)

def filter_files_by_date(file_list, start_date=None, end_date=None):
    filtered_files = []
    for file in file_list:
        date_str = file.split('_')[-1].split('.')[0]
        file_date = datetime.strptime(date_str, "%Y%m%d")
        if ((start_date is None or file_date >= start_date) and 
            (end_date is None or file_date <= end_date)):
            filtered_files.append(file)
    return filtered_files

def combine_csv_files(file_list):
    combined_df = pd.concat((pd.read_csv(file, encoding='SHIFT_JIS') for file in file_list))
    return combined_df

csv_files = get_csv_files("data/*/*/*.csv")

start_date = datetime(2023, 4, 1)  # set the start date as needed
end_date = datetime(2023, 5, 31)  # set the end date as needed
filtered_files = filter_files_by_date(csv_files, start_date, end_date)

# Combine the CSV files
combined_df = combine_csv_files(filtered_files)

# Sort the combined DataFrame by date if the date column exists and has a 'YYYYMMDDHHMM' format
combined_df['日時'] = pd.to_datetime(combined_df['日時'], format='%Y%m%d%H%M')
combined_df = combined_df.sort_values(by='日時')

# Replace the header with English column names and remove '_bid' from the names
combined_df.columns = [
    'date', 
    'open', 
    'high', 
    'low', 
    'close', 
    'open_ask', 
    'high_ask', 
    'low_ask', 
    'close_ask'
]

# Keep only the date and close columns
combined_df = combined_df[['date', 'open', 'high', 'low', 'close']]

# Save the result to a new CSV file called 'combined_data.csv'
combined_df.to_csv("test_combined_data.csv", index=False)
