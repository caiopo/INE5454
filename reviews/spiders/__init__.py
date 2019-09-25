import re
from time import sleep

import scrapy
from scrapy.http import Response
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver

from reviews.items import Product, Review

stars = re.compile('width: 20%')


class ReviewSpider(scrapy.Spider):
    name = 'reviewsbot'
    start_urls = [
        # Ponto Frio parece não estar funcionando
        # 'https://www.pontofrio.com.br/eletrodomesticos/geladeiraerefrigerador/2portas/refrigerador'
        # '-consul-crm51ak-frost-free-bem-estar-com-interface-touch-e-porta-latas-flex-405l-evox-2345969.html',

        'https://www.magazineluiza.com.br/geladeira-consul-frost-free-duplex-405'
        '-litros-cor-inox-com-filtro-bem-estar-/p/8255316/ed/ref2/',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response: Response):
        print(response.url)
        self.prepare_page(response)
        yield from self.scrape_links(response)
        yield from self.scrape_data(response)

    def prepare_page(self, response):
        driver: WebDriver = response.meta['driver']

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        sleep(5)

        try:
            while True:
                element = driver.find_element_by_class_name('product-review__btn-view-more')

                if not element.is_displayed():
                    break

                ActionChains(driver).move_to_element(element).click(element).perform()

                sleep(5)

        except (NoSuchElementException, ElementNotInteractableException) as e:
            print(e)

    def scrape_data(self, response):
        reviews = []

        for review in response.css('.wrapper-review__comment'):
            title = review.css('.product-review__text-content--title::text').get()
            comment = review.css('p.product-review__text-content::text').get()
            rating = len(stars.findall(review.css('.rating-percent__full').get()))
            date = review.css('product-review__text-highlight::text').get()

            reviews.append(
                Review(
                    comment=f'{title}\n{comment}',
                    rating=rating,
                    date=date,
                )
            )

        name = response.xpath('//h1/text()').get()

        product = Product(name=name, url=response.url, reviews=reviews)

        # print(product)

        yield product

    def scrape_links(self, response):
        for showcase in response.css('.showcase__link-product'):
            next_page = showcase.attrib['href']

            yield SeleniumRequest(url=next_page, callback=self.parse, wait_time=10)
