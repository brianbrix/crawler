from concurrent.futures import ThreadPoolExecutor

import googlesearch

import logging
import os
import pandas as pd
import re
import scrapy
from PyQt5.QtCore import QThreadPool
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

#https://medium.com/@rodrigonader/web-scraping-to-extract-contact-information-part-1-mailing-lists-854e8a8844d2
from thread_func import ThreadWorker
from validate_emails import verify_results


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
        print('Cleaning the save file...')
        df = pd.read_csv(self.path, index_col=0)
        df.columns = ['email', 'link']
        df = df.drop_duplicates(subset='email')
        df = df.reset_index(drop=True)
        df.to_csv(self.path, mode='w', header=True)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return
        print("Searching for emails...")
        html_text = str(response.text)
        rgx = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        mail_list = re.findall(rgx, html_text)



        dic = {'email': mail_list, 'link': str(response.url)}
        # worker = ThreadWorker(verify_results, dic, self.path)
        # with ThreadPoolExecutor(max_workers=5) as executor:
        #     future = executor.submit(verify_results, dic,self.path)
        #     print(future.result())
        # th= ThreadPoolExecutor(5)
        # worker = th.submit(verify_results, dic,self.path)
        # self.threadpool.start(worker)
        verify_results(dic, self.path)
        # df = pd.DataFrame(dic)
        # print(df)
        #
        # df.to_csv(self.path, mode='a', header=False)
        # df.to_csv(self.path, mode='a', header=False)
