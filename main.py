import json
import os
import pandas as pd

# Define the directories
json_folder_path = "assets/json_files"
csv_folder_path = "assets/csv_files"

# Ensure the output directory exists
os.makedirs(csv_folder_path, exist_ok=True)


# Helper function to safely extract keys
def safe_get(dictionary, key, default=""):
    try:
        value = dictionary.get(key)
        if value and isinstance(value, dict) and "S" in value:
            return value["S"].replace("\n", "")
    except AttributeError:
        return default
    return default


# Process all JSON files in the folder
for filename in os.listdir(json_folder_path):
    if filename.endswith(".json"):
        json_file_path = os.path.join(json_folder_path, filename)
        csv_file_path = os.path.join(csv_folder_path, f"{os.path.splitext(filename)[0]}.csv")

        extractedData = []

        print(f"Processing file: {filename}")

        with open(json_file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # Load the JSON object and extract the "Item"
                    item_data = json.loads(line.strip()).get("Item", {})
                    if not item_data:
                        print(f"Line {line_number}: Skipping, 'Item' is missing or None")
                        continue

                    # Extract and clean fields
                    questionId = safe_get(item_data, "questionId")
                    questionTitleHtml = safe_get(item_data, "questionTitleHtml")
                    questionType = safe_get(item_data, "questionType")

                    # Process questionOptions
                    options = []
                    questionOptions_raw = item_data.get("questionOptions", {}).get("M")
                    if questionOptions_raw and isinstance(questionOptions_raw, dict):
                        options = [value["S"].strip().replace("\n", "") for value in questionOptions_raw.values()]
                    questionOptions = ";;".join(options)

                    # Extract questionStatus
                    questionStatus = safe_get(item_data, "questionStatus")

                    # Process allTagsIdValueMapping
                    allTagsIdValueMapping_raw = item_data.get("allTagsIdValueMapping", {}).get("S")
                    try:
                        allTagsIdValueMapping = (
                            json.loads(allTagsIdValueMapping_raw) if allTagsIdValueMapping_raw else {}
                        )
                    except json.JSONDecodeError:
                        allTagsIdValueMapping = {}

                    # Safely retrieve the values for clientRef keys
                    def get_value(client_ref):
                        value_dict = allTagsIdValueMapping.get(client_ref, {})
                        if isinstance(value_dict, dict):
                            return next(iter(value_dict.values()), "")
                        return ""

                    # Extract clientRef values
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
                        "exam_category": exam_category.replace("\n", ""),
                        "sub_category": sub_category.replace("\n", ""),
                        "subject_name": subject_name.replace("\n", ""),
                        "chapter_name": chapter_name.replace("\n", ""),
                        "subtopic_name": subtopic_name.replace("\n", ""),
                    }

                    # Append cleaned data
                    extractedData.append(format_for_csv)

                except json.JSONDecodeError as e:
                    print(f"Line {line_number}: Skipping invalid JSON: {e}")
                except Exception as e:
                    print(f"Line {line_number}: Unexpected error: {e}")

        # Convert data to DataFrame and save to CSV
        if extractedData:
            df = pd.DataFrame(extractedData)
            df.to_csv(csv_file_path, index=False, encoding="utf-8")
            print(f"CSV saved successfully at {csv_file_path}")
        else:
            print(f"No valid data to write for {filename}.")
