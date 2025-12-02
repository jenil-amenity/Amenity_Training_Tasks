import os
import shutil
import csv
import json

# copy file 
# src = 'data.csv'
# des = 'test2.txt'
# res = shutil.copyfile(src, des)
# print(res)

#copy folder with files
# src = r'folder1/test2.txt'
# des = r'folder3'

# os.makedirs(des, exist_ok=True)

# des_path= shutil.copy2(src, des)
# print(f"Copied to >> {des_path}")

# Copy nested folders

# src = 'folder2'
# des = 'folder5'

# try:
#     des_path= shutil.copytree(src, des)
#     print(f"Copied to >> {des_path}")
# except Exception as e:
#     print(e)

#copy Folder
# src = 'folder4'
# des = 'folder6'

# try:
#     des_path= shutil.copytree(src, des)
#     print(f"Copied to >> {des_path}")
# except Exception as e:
#     print(e)

# csv File RW   
# file = open('data.csv','r')
# reader = csv.reader(file)
# for row in reader:
#     print(" | ".join(row))
# file.close()

# CSV WRITE
# with open('data.csv',"a") as f:
#     f.write("Joseph,39,India")

# with open('data.csv',"r") as f:
#     print(f.read())

# Text File READ
# file = open('test.txt','r')
# print(file.read())
# file.close()

# TEXT FILE READ
# with open("test.txt", "a") as wt:
#     wt.writelines("Steve Harington")

# with open('test.txt',"r") as f:
#     print(f.read())


# # JSON file read
# file = open('tata.json')
# rjson = json.load(file)
# print(json.dumps(rjson, indent=5))
# file.close()

#JSON write
data = {
    "id": "2",
    "name": "Suresh",
    "Age":"21"
}
with open("tata.json", "w") as jw:
    json.dump(data, jw, indent=2)

# Read it back
with open("tata.json") as jr:
    rjson = json.load(jr)
    print(json.dumps(rjson, indent=2))
    