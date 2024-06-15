import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Load URLs from external JSON file
with open('urls.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    urls = data['urls']

# Open the output file in write mode
with open('news_notices.txt', 'w', encoding='utf-8') as file:
    for URL in tqdm(urls, desc="Processing URLs"):
        try:
            page = requests.get(URL)
            page.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(page.content, "html.parser")

            element = soup.find('div', class_="view-content")
            
            if element:
                text_content = element.get_text(separator=' | ', strip=True)
                file.write(f"Text from {URL}:\n{text_content}\n\n")
            else:
                file.write(f"Could not find the content in {URL}\n\n")

        except requests.exceptions.RequestException as e:
            file.write(f"An error occurred while fetching {URL}: {e}\n\n")

print("Content has been written to news_notices.txt")
