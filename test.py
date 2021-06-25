import json

with open("dict2.json") as f:
    file = json.load(f)

print(file["fighting"]["normal"])
