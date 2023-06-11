import json
import logging
from requests_html import HTMLSession
import os


class MubawabScraper:
    start_urls = ["https://www.mubawab.ma/fr/st/casablanca/appartements-a-vendre"]
    proxies = [
        "2.56.119.93:5074:qtenooge:syncclqsof43",
        "185.199.229.156:7492:qtenooge:syncclqsof43",
        "185.199.228.220:7300:qtenooge:syncclqsof43",
        "185.199.231.45:8382:qtenooge:syncclqsof43",
        "188.74.210.207:6286:qtenooge:syncclqsof43",
        "188.74.183.10:8279:qtenooge:syncclqsof43",
        "188.74.210.21:6100:qtenooge:syncclqsof43",
        "45.155.68.129:8133:qtenooge:syncclqsof43",
        "154.95.36.199:6893:qtenooge:syncclqsof43",
        "45.94.47.66:8110:qtenooge:syncclqsof43"
    ]

    def __init__(self):
        logging.basicConfig(filename='../logs/scraper.log', level=logging.INFO)
        self.proxy_index = 0

        # Format proxies correctly for requests
        self.proxies = [f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}" for proxy in self.proxies]

    def scrape(self):
        session = HTMLSession()
        data = []
        file_path = os.path.abspath('../data/immo_data.json')

        for url in self.start_urls:
            logging.info(f'Scraping URL: {url}')
            page_data = self.scrape_page(session, url, file_path, 1)
            data.extend(page_data)

    def scrape_page(self, session, url, file_path, page_num):
        print(f"Scraping page: {url}")
        try:
            response = session.get(url, proxies={"http": self.proxies[self.proxy_index], "https": self.proxies[self.proxy_index]})
            response.html.render(timeout=20)  # Execute JavaScript with a 20 second timeout
        except Exception as e:
            logging.error(f'Error occurred while getting page: {e}')
            return []

        data = []
        for property in response.html.find('li.listingBox'):
            property_data = self.parse_property(property)
            if property_data is not None:
                data.append(property_data)

        self.save_to_json(file_path, data)

        next_button = response.html.xpath('/html/body/section/div[2]/div[3]/div[3]/a[9]', first=True)
        if next_button:
            next_url = next_button.absolute_links.pop()
            logging.info(f'Navigating to next page: {next_url}')

            # Rotate proxies every 5 pages
            if page_num % 5 == 0:
                self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
                logging.info(f'Changing to proxy {self.proxy_index}: {self.proxies[self.proxy_index]}')

            page_data = self.scrape_page(session, next_url, file_path, page_num+1)
            data.extend(page_data)  # Add the next page's data to this page's data
        else:
            logging.info('No next button found')

        return data

    def parse_property(self, property):
        logging.info('Parsing property')
        try:
            link = property.xpath('//li/@linkref', first=True)

            property_id = property.xpath('.//input[@class="adId"]/@value', first=True)

            price_element = property.find('.priceTag', first=True)
            price = price_element.text if price_element else None

            title_element = property.find('h2.listingTit a', first=True)
            title = title_element.text if title_element else None

            size_and_rooms_element = property.find('h4.listingH4', first=True)
            size_and_rooms = size_and_rooms_element.text if size_and_rooms_element else None

            location_element = property.find('h3.listingH3', first=True)
            location = location_element.text if location_element else None

            description_element = property.find('p.listingP', first=True)
            description = description_element.text if description_element else None

            images = [img.attrs.get('src') or img.attrs.get('data-lazy') for img in property.find('img.sliderImage')]

            logging.info('Property parsed successfully')
            property_data = {
                'link': link,
                'property_id': property_id,
                'price': price,
                'title': title,
                'size_and_rooms': size_and_rooms,
                'location': location,
                'description': description,
                'images': images
            }
            logging.info(f'Property data: {property_data}')
            return property_data

        except Exception as e:
            logging.error(f'Error occurred while parsing property: {e}')
            return None

    @staticmethod
    def save_to_json(file_path, data):
        with open(file_path, 'a', encoding='utf_8') as f:
            for item in data:
                json.dump(item, f, ensure_ascii=False)
                f.write('\n')

        logging.info(f'Data appended to {file_path}')


if __name__ == "__main__":
    scraper = MubawabScraper()
    scraper.scrape()
