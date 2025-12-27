import os
import shutil
import csv
import json

def copy_file(src, des):
    return shutil.copyfile(src, des)

def copy_folder_with_files(src, des):
    os.makedirs(des, exist_ok=True)
    return shutil.copy2(src, des)

def copy_nested_folders(src, des):
    return shutil.copytree(src, des)

def read_csv(path):
    with open(path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(" | ".join(row))

def write_csv(path, row):
    with open(path, "a", newline="") as f:
        f.write(row)

def read_text(path):
    with open(path, "r") as f:
        return f.read()

def write_text(path, text):
    with open(path, "a") as f:
        f.write(text)

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    data = {
        "id": "2",
        "name": "Suresh",
        "Age": "21"
    }

    write_json("tata.json", data)
    result = read_json("tata.json")

    print(json.dumps(result, indent=2))
