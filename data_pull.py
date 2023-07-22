from time import sleep
import requests
import json
import os

# Specify the path to the JSON file
json_file = 'constituencyList.json'
# Load JSON data from the file
with open(json_file, 'r') as file:
    data = json.load(file)


def save_html(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Saved {filename}")
    else:
        print(f"Failed to save {url}")

folder = 'election_live_results'
roundwise_folder = os.path.join(folder, 'roundwise')
constituencywise_folder = os.path.join(folder, 'constituencywise')

if not os.path.exists(folder):
    os.makedirs(folder)

if not os.path.exists(roundwise_folder):
    os.makedirs(roundwise_folder)

if not os.path.exists(constituencywise_folder):
    os.makedirs(constituencywise_folder)

# Access the loaded JSON data
for key, value in data.items():
    #Roundwise
    url1 = f'https://results.eci.gov.in/ResultAcGenMay2023/RoundwiseS10{key}.htm?ac={key}'
    filename1 = os.path.join(roundwise_folder, f'RoundwiseS10{key}.htm')
    save_html(url1, filename1)
    # Constituencywise
    url2 = f'https://results.eci.gov.in/ResultAcGenMay2023/ConstituencywiseS10{key}.htm?ac={key}'
    filename2 = os.path.join(constituencywise_folder, f'ConstituencywiseS10{key}.htm')
    save_html(url2, filename2)
    sleep(0.3)

