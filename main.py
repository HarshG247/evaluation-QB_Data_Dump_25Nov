import json
import os
import pandas as pd

# Define the file paths
json_file_path = "assets/json_files/b4e6jlgyou6b7hnivud4c4quj4.json"
csv_file_path = "assets/csv_files/file-1_b4e6jlgyou6b7hnivud4c4quj4.csv"  # Include the file name for the CSV


# Helper function to safely extract keys
def safe_get(dictionary, key, default=""):
    try:
        return dictionary[key]["S"].replace("\n", "")
    except KeyError:
        return default


# Read and process multiple JSON objects line by line
with open(json_file_path, "r", encoding="utf-8") as file:
    extractedData = []
    for line_number, line in enumerate(file, start=1):
        try:
            # Load the JSON object and extract the "Item"
            Item = json.loads(line.strip()).get("Item", {})

            # Extract and clean fields with error handling for missing keys
            questionId = safe_get(Item, "questionId")
            questionTitleHtml = safe_get(Item, "questionTitleHtml")
            questionType = safe_get(Item, "questionType")

            # Process questionOptions with error handling
            try:
                options = [value["S"].strip().replace("\n", "") for value in Item["questionOptions"]["M"].values()]
                questionOptions = ";;".join(options)
            except KeyError:
                questionOptions = ""

            # Extract questionStatus
            questionStatus = safe_get(Item, "questionStatus")

            # Process allTagsIdValueMapping with error handling
            try:
                allTagsIdValueMapping_json = Item["allTagsIdValueMapping"]["S"]
                allTagsIdValueMapping = json.loads(allTagsIdValueMapping_json)
            except KeyError:
                allTagsIdValueMapping = {}

            # Safely retrieve values for each clientRef
            def get_value(client_ref):
                return next(iter(allTagsIdValueMapping.get(client_ref, {}).values()), "")

            # Extract tag values
            exam_category = get_value("clientRef1")
            sub_category = get_value("clientRef2")
            subject_name = get_value("clientRef3")
            chapter_name = get_value("clientRef4")
            subtopic_name = f"{get_value('clientRef5')};;{get_value('clientRef6')}"

            # Populate the CSV format
            format_for_csv = {
                "questionId": questionId,
                "questionTitleHtml": questionTitleHtml,
                "questionType": questionType,
                "questionOptions": questionOptions,
                "questionStatus": questionStatus,
                "exam_category": exam_category.replace("\n", ""),  # clientRef1
                "sub_category": sub_category.replace("\n", ""),  # clientRef2
                "subject_name": subject_name.replace("\n", ""),  # clientRef3
                "chapter_name": chapter_name.replace("\n", ""),  # clientRef4
                "subtopic_name": subtopic_name.replace("\n", ""),  # clientRef5;;clientRef6
            }

            # Append cleaned data
            extractedData.append(format_for_csv)

        except json.JSONDecodeError as e:
            print(f"Line {line_number}: Skipping invalid JSON: {e}")
        except Exception as e:
            print(f"Line {line_number}: Unexpected error: {e}")

    # Convert data to DataFrame
    if extractedData:
        print("Converting...")
        df = pd.DataFrame(extractedData)
        # Save the DataFrame to a CSV file
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)  # Ensure the directory exists
        df.to_csv(csv_file_path, index=False, encoding="utf-8")
        print(f"CSV saved successfully at {csv_file_path}")
    else:
        print("No valid data to write to CSV.")
