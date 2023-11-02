import json
from pathlib import Path
import os.path

file_path = 'bd.json'

if os.path.exists(file_path) == False:
    with open(file_path,'w') as file: 
        bd = {}
        json.dump(bd, file)

contact = {
  "iana": [
    {
      "address": 'brovary',
      "phone": [8765467890],
      "email": 'tara@gmail.com',
      "birthdate": '2000-01-01'
    }
  ]
}
with open(file_path) as file:
    data = json.load(file)
    for key, value in contact.items():
         if key in data.keys():
             data.pop(key)
    data[key] = value

with open(file_path,'w') as file: 
    json.dump(data, file, indent=2, ensure_ascii=False)  
