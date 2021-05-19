import googlesearch

import logging
import os
import pandas as pd
import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

#https://medium.com/@rodrigonader/web-scraping-to-extract-contact-information-part-1-mailing-lists-854e8a8844d2
class MailSpider(scrapy.Spider):
    name = 'email'

    def __init__(self, path, reject, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.reject = reject

    def parse(self, response):
        """

        :param response:
        """
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return
        print("Searching for emails...")
        html_text = str(response.text)
        rgx = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        mail_list = re.findall(rgx, html_text)

        dic = {'email': mail_list, 'link': str(response.url)}
        df = pd.DataFrame(dic)
        print(df)

        df.to_csv(self.path, mode='a', header=False)
        # df.to_csv(self.path, mode='a', header=False)
