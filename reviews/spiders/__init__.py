from time import sleep

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver


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
            print(url)
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=3)

    def parse(self, response):
        driver: WebDriver = response.meta['driver']

        sleep(3)

        try:
            while True:
                element = driver.find_element_by_class_name('product-review__btn-view-more')

                if not element.is_displayed():
                    break

                ActionChains(driver).move_to_element(element).click(element).perform()
                sleep(3)

        except (NoSuchElementException, ElementNotInteractableException) as e:
            print(e)

        name = response.xpath('//h1/text()').get()
