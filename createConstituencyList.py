from bs4 import BeautifulSoup
import json
import os

folder = 'election_live_results'
def extract_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')

        # Use BeautifulSoup methods to extract data from the HTML page
        # For example:
        title = soup.title.text
        paragraphs = soup.find_all('p')
        links = [a['href'] for a in soup.find_all('a')]

        # Return the extracted data
        return title, paragraphs, links


def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)

def find_input_with_id(filename, element_id):
    with open(filename, 'r', encoding='utf-8') as file:
        html = file.read()
        soup = BeautifulSoup(html, 'html.parser')
        # Find the input element with the specified id
        input_element = soup.find('input', {'id': element_id})
        # Extract the value from the input element
        if input_element:
            value = input_element.get('value')
            values_list = value.split(';')

            # Extract the id and value pairs
            extracted_data = {}
            for pair in values_list:
                id_value = pair.split(',')
                if len(id_value) == 2:
                    element_id = id_value[0]
                    element_value = id_value[1]
                    extracted_data[element_id] = element_value

            return extracted_data

        return None


filename1 = os.path.join(folder, 'RoundwiseS1034.htm')
info = find_input_with_id(filename1, 'S10')
save_json_to_file(info, 'constituencyList.json')