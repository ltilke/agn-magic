import json
import os

with open('blank_config.json') as f:
  data = json.load(f)

# Output: {'name': 'Bob', 'languages': ['English', 'Fench']}

data['wavelengths'] = {'B': 'Purple'}
print(data)
with open('config.json', mode='w') as f:
    json.dump(data, f)
