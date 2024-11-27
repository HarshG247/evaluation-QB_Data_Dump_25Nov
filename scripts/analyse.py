import pandas as pd

# Read the CSV file
combined_output = pd.read_csv("assets/csv_files/output/combined_output.csv")

# Filter questions that are not empty and have `questionStatus` as "PUBLISHED"
filtered_questions = combined_output[
    combined_output["questionTitleHtml"].notnull() & (combined_output["questionStatus"] == "PUBLISHED")
]

# Check how many rows have empty values for the specified columns
columns_to_check = ["category", "exam", "subject", "topic", "subtopic", "chapter_name"]
empty_counts = filtered_questions[columns_to_check].isnull().sum()

# Get the total number of rows in the dataset and filtered dataset
total_rows = len(combined_output)
filtered_total_rows = len(filtered_questions)

# Display the results
print(f"Total number of rows in the CSV: {total_rows}")
print(f"Number of questions with `questionTitleHtml` not empty and `questionStatus` published: {filtered_total_rows}")
print("Number of empty values per column (in the filtered dataset):")
print(empty_counts)
