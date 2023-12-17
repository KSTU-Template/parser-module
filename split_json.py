import json
import os

def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def split_and_save(data):
    for category, subcategories in data.items():
        category_filename = f"{category}.json"
        save_to_file({category: subcategories}, category_filename)
        with open(f"{category}.txt", 'w', encoding='utf-8') as text_file:
            write_data_to_file({category: subcategories}, file=text_file)

def write_data_to_file(data, indentation=0, file=None):
    for key, value in data.items():
        if isinstance(value, dict):
            file.write(f"{'  ' * indentation}{key}:\n")
            write_data_to_file(value, indentation + 1, file)
        elif isinstance(value, list):
            file.write(f"{'  ' * indentation}{key}:\n")
            for item in value:
                if isinstance(item, dict):
                    write_data_to_file(item, indentation + 1, file)
                else:
                    file.write(f"{'  ' * (indentation + 1)}- {item}\n")
        else:
            file.write(f"{'  ' * indentation}{key}: {value}\n")


with open("redacted_info.json", 'r', encoding='utf-8') as json_file:
    data = json.load(json_file, strict=False)

if __name__ == "__main__":
    with open('redacted_info.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    split_and_save(data)