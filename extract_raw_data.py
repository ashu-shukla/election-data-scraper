from bs4 import BeautifulSoup
import json
import os


json_file = 'constituencyList.json'
with open(json_file, 'r') as file:
    data = json.load(file)

folder = 'election_live_results'
roundwise_folder = os.path.join(folder, 'roundwise')
constituencywise_folder = os.path.join(folder, 'constituencywise')

def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


def constituency_wise(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', {'id': 'div1'})
        table = div.find("table")
        extracted_data = []
        if table:
            table_body = table.find('tbody')
            headers = [th.text.strip() for th in table_body.find_all('th')]
            rows = [[td.text.strip() for td in tr.find_all('td')]
                    for tr in table_body.find_all('tr')[3:-1]]
            for row in rows:
                row_data = {}
                for index, header in enumerate(headers[1:]):
                    row_data[header] = row[index+1]
                extracted_data.append(row_data)
            return extracted_data
        return None

def round_wise(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', {'class': 'all-tabs'})
        extracted_data = {}
        if div:
            tabs = div.find_all('div', {'class': 'tabcontent'})
            for tab in tabs:
                table_data = []
                if tab.has_attr('id'):
                    round_id = tab['id'].replace('tab','')
                    table = tab.find("table")
                    if table:
                        table_body = table.find('tbody')
                        table_headers = table.find('thead')
                        headers = [th.text.strip() for th in table_headers.find_all('th')]
                        rows = [[td.text.strip() for td in tr.find_all('td')]
                                for tr in table_body.find_all('tr')]
                        for row in rows:
                            row_data = {}
                            for index, header in enumerate(headers[2:]):
                                row_data[header] = row[index]
                            table_data.append(row_data)
                extracted_data[round_id] = table_data
            return extracted_data


roundwise_js = {}
constituencywise_js = {}


for key, value in data.items():
    filename = os.path.join(constituencywise_folder, f'ConstituencywiseS10{key}.htm')
    info = constituency_wise(filename)
    filename2 = os.path.join(roundwise_folder, f'RoundwiseS10{key}.htm')
    info2 = round_wise(filename2)
    constituencywise_js[value] = info
    roundwise_js[value] = info2

save_json_to_file(constituencywise_js, 'constituencyWise.json')
save_json_to_file(roundwise_js, 'roundWise.json')
