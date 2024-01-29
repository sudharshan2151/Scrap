import requests
from bs4 import BeautifulSoup
import json
import gzip

class FlipkartScraper:

    def __init__(self, base_url, user_agent):
        self.base_url = base_url
        self.headers = {'User-Agent': user_agent}

    def scrape_flipkart(self, pincode):
        search_url = f"{self.base_url}/search?q=laptops&pincode={pincode}"
        response = requests.get(search_url, headers=self.headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            laptop_elements = soup.select('div._1AtVbE')

            laptops = []
            for laptop_element in laptop_elements:
                sku_id = laptop_element.get('data-tkid')
                
                product_name_element = laptop_element.select_one('div._4rR01T')
                product_name = product_name_element.get_text(strip=True) if product_name_element else None

                product_title_element = laptop_element.select_one('a._2mylT6')
                product_title = product_title_element.get('title') if product_title_element else None
                description = product_title_element.get('title') if product_title_element else None

                laptops.append({
                    'sku_id': sku_id,
                    'product_name': product_name,
                    'product_title': product_title,
                    'description': description
                })

            return laptops

        else:
            print(f"Failed to fetch data from {search_url}. Status Code: {response.status_code}")
            return None


    def save_to_gzip_ndjson(self, data, pincode):
        file_name = f"flipkart_laptops_{pincode}.ndjson.gz"
        with gzip.open(file_name, 'wt', encoding='utf-8') as f:
            for laptop in data:
                f.write(json.dumps(laptop) + '\n')

def main():
    flipkart_scraper = FlipkartScraper(base_url='https://www.flipkart.com', user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

    pincodes = ['560001', '110001']
    for pincode in pincodes:
        laptops_data = flipkart_scraper.scrape_flipkart(pincode)
        if laptops_data:
            flipkart_scraper.save_to_gzip_ndjson(laptops_data, pincode)
            print(f"Data for pincode {pincode} saved successfully.")

if __name__ == "__main__":
    main()
