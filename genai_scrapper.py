import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

class GenAiScrapper:

    def __init__(self):
        pass

    def import_csv_module(self, file_name: str = "msft_partner.csv", folder_path = r'C:\Users\karth\Downloads\GenAI_Website_Content_Evaluation', content: str = '', df: str = '', website = None):
        self.file_name = file_name
        self.folder_path = folder_path
        self.content = content
        self.df = df
        self.website = []

        path = os.path.join(self.folder_path, self.file_name)

        try:
            self.df = pd.read_csv(path)

        except FileNotFoundError as e:
            print(f"File Not found!! {e}")
            return

        column_to_check = ['website','Website', 'web', 'webpage']
        
        columns_found = any(col in self.df.columns for col in column_to_check)
        if columns_found:
            self.website = self.df['Website'].dropna().tolist()
        else:
            print("No such column found")


    def scrape_website(self, scraped_text = None):
        self.scraped_text = []

        if not self.website:
            print("No website found")
            return
        
        for url in self.website:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:  
                    soup = BeautifulSoup(response.text, 'html.parser') 
                    text = soup.get_text(separator=" ", strip=True)
                    self.scraped_text.append(text)
                    print(f"Successfully fetched for url: {url}")
                else:
                    print("Unable to fetch")
                    self.scraped_text.append("Error: Unable to fetch")
            except Exception as e:
                self.scraped_text.append(f"Error: {e}")

        self.df['scraped_text'] = self.scraped_text
        self.df.to_csv("output.csv", index=False)

    def text_normalization(self, file = 'output.csv', folder = r'C:\Users\karth\Downloads\GenAI_Website_Content_Evaluation', df1: str = '', clean_text_list = None):
        self.file = file
        self.folder = folder
        self.df1 = df1
        self.clean_text_list = []

        error = 'Error: HTTPSConnectionPool'

        path = os.path.join(self.folder, self.file)

        try:
            self.df1 = pd.read_csv(path)
        except Exception as e:
            print(f"Error Reading file: {e}")

        if 'scraped_text' in self.df1.columns:
            for text in self.df1['scraped_text']:
                if error not in text:
                    clean_text = re.sub(r'\s+', ' ', text).strip()
                    self.clean_text_list.append(clean_text)
                else:
                    clean_text = 'N/A'
                    self.clean_text_list.append(clean_text)

        cleaned_text = self.clean_text_list

        self.df1['clean_text'] = cleaned_text

        self.df1.to_csv(path, index=False)

        


    def main(self):
        self.import_csv_module()
        self.scrape_website()
        self.text_normalization()

if __name__ == '__main__':
    run_scraper = GenAiScrapper()
    run_scraper.main()
