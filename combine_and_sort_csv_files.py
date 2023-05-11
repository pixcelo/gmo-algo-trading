import pandas as pd
import glob

def get_csv_files(path_pattern):
    return glob.glob(path_pattern)

def combine_csv_files(file_list):
    combined_df = pd.concat((pd.read_csv(file, encoding='SHIFT_JIS') for file in file_list))
    return combined_df

csv_files = get_csv_files("data/*/*/*.csv")

# Combine the CSV files
combined_df = combine_csv_files(csv_files)

# Sort the combined DataFrame by date if the date column exists and has a 'YYYYMMDDHHMM' format
combined_df['日時'] = pd.to_datetime(combined_df['日時'], format='%Y%m%d%H%M')
combined_df = combined_df.sort_values(by='日時')

# Replace the header with English column names
combined_df.columns = [
    'date', 
    'open_bid', 
    'high_bid', 
    'low_bid', 
    'close_bid', 
    'open_ask', 
    'high_ask', 
    'low_ask', 
    'close_ask'
]

# Save the result to a new CSV file called 'combined_data.csv'
combined_df.to_csv("combined_data.csv", index=False)
