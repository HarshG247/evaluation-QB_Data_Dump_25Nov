import os
import pandas as pd

# Load the CSV files
file1 = 'assets/csv_files/questions_combined_output.csv'
file2 = 'assets/csv_files/solutions_combined_output.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Merge the two DataFrames on the key column 'questionId'
combined = pd.merge(df1, df2, on='questionId')


# Define the output directory and file name
output_directory = 'assets/csv_files/output/'
output_file = 'combined_output.csv'

# Ensure the output directory exists (you might need to create it if it doesn't)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Save the combined DataFrame to a new CSV file
combined.to_csv(os.path.join(output_directory, output_file), index=False)