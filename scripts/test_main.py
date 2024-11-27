import json
import os
import pandas as pd

# Define the directories
json_folder_path = "assets/json_files/solutions"
csv_folder_path = "assets/csv_files/solutions"
combined_csv_path = "assets/csv_files/solutions_combined_output.csv"  # Final combined CSV file

# Ensure the output directory exists
os.makedirs(csv_folder_path, exist_ok=True)


# Helper function to safely extract nested dictionary values
def safe_get(dictionary, keys, default=""):
    try:
        for key in keys:
            dictionary = dictionary.get(key, {})
        return dictionary if isinstance(dictionary, str) else default
    except AttributeError:
        return default


# List to hold data from all files
combined_data = []

# Process all JSON files in the folder
for filename in os.listdir(json_folder_path):
    if filename.endswith(".json"):
        json_file_path = os.path.join(json_folder_path, filename)
        csv_file_path = os.path.join(csv_folder_path, f"{os.path.splitext(filename)[0]}.csv")

        extractedData = []

        print("\n##########################")
        print(f"Processing file: {filename}")

        with open(json_file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # Load the JSON object and extract the "Item"
                    item_data = json.loads(line.strip()).get("Item", {})
                    if not item_data:
                        print(f"Line {line_number}: Skipping, 'Item' is missing or None")
                        continue

                    # Extract and clean fields using safe_get
                    questionId = safe_get(item_data, ["questionId", "S"])
                    modifiedAt = safe_get(item_data, ["modifiedAt", "N"])
                    answerId = safe_get(item_data, ["answerId", "S"])
                    createdAt = safe_get(item_data, ["createdAt", "N"])
                    explanationText = safe_get(item_data, ["explanationText", "S"])
                    answer = safe_get(item_data, ["answer", "S"])
                    explanation_Correct = safe_get(item_data, ["explanation", "M", "Correct", "S"])
                    explanationSolution = safe_get(item_data, ["explanation", "M", "Solution", "S"])

                    # Populate the CSV format
                    format_for_csv = {
                        "questionId": questionId.replace("\n", ""),
                        "modifiedAt": modifiedAt.replace("\n", ""),
                        "answerId": answerId.replace("\n", ""),
                        "createdAt": createdAt.replace("\n", ""),
                        "explanationText": explanationText.replace("\n", ""),
                        "answer": answer.replace("\n", ""),
                        "explanation_Correct": explanation_Correct.replace("\n", ""),
                        "explanationSolution": explanationSolution.replace("\n", ""),
                    }

                    extractedData.append(format_for_csv)

                except json.JSONDecodeError as e:
                    print(f"Line {line_number}: Skipping invalid JSON: {e}")
                except Exception as e:
                    print(f"Line {line_number}: Unexpected error: {e}")

        # Convert data to DataFrame and save to a CSV file
        if extractedData:
            df = pd.DataFrame(extractedData)
            df.to_csv(csv_file_path, index=False, encoding="utf-8")
            combined_data.extend(extractedData)
            print(f"CSV saved successfully at {csv_file_path}")
        else:
            print(f"No valid data to write for {filename}.")

# Combine all data into a single CSV
if combined_data:
    combined_df = pd.DataFrame(combined_data)
    combined_df.to_csv(combined_csv_path, index=False, encoding="utf-8")
    print(f"Combined CSV saved successfully at {combined_csv_path}")
else:
    print("No data to combine.")
