import time
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService

from bs4 import BeautifulSoup
import requests

# def get_driver():
#     # path of the chromedriver we have just downloaded
#     PATH = f"./chromedriver.exe"
#     driver = webdriver.Chrome()  # to open the browser
#     # # url of google news website

#     # url = 'https://safeway.com'

#     # # to open the url in the browser
#     # driver.get(url)
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('excludeSwitches', ['enable-logging'])


#     browser = webdriver.Chrome(service=ChromiumService(PATH),options=options)
#     driver.get('https://www.walmart.com')
#     title = "/html/body/div/div[1]/div/div/div[2]/div/main/div/div/div/div/section[1]/div/div/section/a[2]"
#     link = driver.find_element_by_xpath(title)
#     print(link.text)


# def main():
#     get_driver()


class WebScraper:
    SAFEWAY = "https://www.safeway.com/shop/aisles.3132.html"
    INDEPENDENT = "https://www.yourindependentgrocer.ca/"
    WALMART = "https://www.walmart.com/all-departments"

    def __init__(self):
        self.website = [self.SAFEWAY, self.INDEPENDENT, self.WALMART]
        self.driver = webdriver.Chrome()

    def scrape(self):
        self.request_website()

    def request_website(self):
        self.driver.get(self.website[2])
        html = self.driver.page_source
       # print(html)
        soup = BeautifulSoup(html, "html.parser")
        # print(soup.prettify())
        item_hyperlinks = soup.find_all("div", class_="w_KPWk w_GxNv mh2 ph2 ph1-xl mb4 pb3")
        print(item_hyperlinks)
        for item in item_hyperlinks:
            print(item["href"])
            category = self.driver.get(f"{self.website}{item['href']}")
            category_soup = BeautifulSoup(self.driver.page_source, "html.parser")
            print(category_soup.prettify())
            break
        # while True:
        #     pass

    #     req = requests.get(self.website).text
    #     soup = BeautifulSoup(req, 'lxml')
    #     #print(soup.prettify())
    #     aisle_items = soup.find_all('div', class_="col-12 col-sm-12 col-md-4 col-lg-4 col-xl-3")

    #     for item in aisle_items:
    #         link = item.find('a')["href"]
    #         print(link)

    #         next_req = requests.get(f"{self.website}{link}")
    #         print(next_req.content)
    #         next_soup = BeautifulSoup(next_req.content, 'html.parser')
    #      #   print(next_soup.prettify())

    #         product_categories = next_soup.find_all('ul', class_="product-subcats")
    #         print(product_categories)
    #    #     self.loop_categories(product_categories)
    #         print("here")
    #         break

    # catergories-item aisle-item


if __name__ == "__main__":
    # main()
    scraper = WebScraper()

    scraper.scrape()
