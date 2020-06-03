# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class ComputerComponentsSpider(scrapy.Spider):
    name = 'computer_components'
    
    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://slickdeals.net/computer-deals/',
            wait_time = 2,
            callback = self.parse
        )

    def parse(self, response):

        for item in response.xpath('//div[@class="fpItem  "]'):
            yield{
                'item': item.xpath('.//div/div/div/div/a/text()').get(),
                'shop': item.xpath('.//div/div/div/div/span/button/text()').get(),
                'price': item.xpath('normalize-space(.//div/div/div[2]/div[2]/div/text())').get(),
                'likes': item.xpath('.//div/div[2]/div/span/span[2]/text()').get(),
                'link': response.urljoin(item.xpath('.//div/div/div/div/a/@href').get())
            }
        
        next_page_button = response.xpath('//a[@data-role = "next-page"]/@href').get()
        if next_page_button:
            yield SeleniumRequest(
                url= response.urljoin(next_page_button),
                wait_time = 2,
                callback = self.parse
            )