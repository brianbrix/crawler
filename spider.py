import asyncio
from datetime import datetime
from functools import partial
from urllib.parse import urlparse

import nltk
import pandas as pd
import re
import scrapy
from PyQt5.QtCore import QThreadPool

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import tldextract
import get_names
from codes import EmailToName
from thread_func import ThreadWorker
from validate_emails import EMailValidate

emails = []
emails_list = set()
from verify_email import verify_email
from bs4 import BeautifulSoup


class MailSpider(scrapy.Spider):
    name = 'email'
    print("here")

    def __init__(self, path, reject, path2, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.reject = reject
        self.path2 = path2
        self.threadpool = QThreadPool()
        self.mails_list = []
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    #
    def closed(self, reason):
        print("closed")
        self.spider_ended()

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(MailSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed, signal=signals.engine_stopped)
    #     return spider
    def spider_ended(self):

        print("Nearing verify...")
        self.valid()
        return 0

    def parse(self, response):
        """

        :param response:
        """
        print("pass")
        links = LxmlLinkExtractor(allow=()).extract_links(response)
        links = [str(link.url) for link in links]
        links.append(str(response.url))

        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)

    def parse_link(self, response):

        for word in self.reject:
            if word in str(response.url):
                return
        d = tldextract.extract(response.url)
        self.domain = f"{d.domain}.{d.suffix}"
        # domain = '{uri.netloc}'.format(uri=parsed_uri)
        print("Searching for emails...")
        html_text = str(response.text)
        soup = BeautifulSoup(html_text)
        self.txt = soup.get_text()
        key_words = ["management" "team", "directors", "executives", "our team", "officials", "team",
                     "board of directors",
                     "executive" "directors", "non executive directors", "staffs", "members", "leaders", "investors"]
        self.mail_list = []
        rgx = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        # rgx = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}'
        if any(word in html_text for word in key_words):
            self.mail_list = re.findall(rgx, html_text)
            dic = {'email': self.mail_list, 'link': str(response.url), "mode": "scraped"}
            df = pd.DataFrame(dic)
            df.to_csv(self.path, mode='a', header=False)
            df.to_csv(self.path, mode='a', header=False)
            print(self.mail_list)

        else:
            worker = ThreadWorker(self.extratc_from_page, response.url)
            self.threadpool.start(worker)

    def valid(self):
        print('Cleaning the save file...')
        df = pd.read_csv(self.path, index_col=0)
        df.columns = ['email', 'link', 'mode']
        df = df.drop_duplicates(subset='email')
        df = df.reset_index(drop=True)
        # dictt = df.to_dict()
        # self.mails_list = [v for k, v in dictt["email"].items() if k >= 1]
        self.mails_list = df.set_index('email')['mode'].to_dict()
        # print("mails", self.mails_list)
        df.to_csv(self.path, mode='w', header=True)
        EMailValidate(self.mails_list, self.path2)
        # m.verify_results(list(set(self.mails_list)), self.path2)
        # worker=ThreadWorker(m.verify_results,list(set(self.mails_list)), self.path2 )
        # self.threadpool.start(worker)

        # self.spider_ended()

    def extratc_from_page(self, link):
        """
        @:param
        """
        mail_list = []
        print("The keywords were not found.")
        people = get_names.get_names(self.txt)
        # print(people)
        for person in people:
            names = person.split(" ")
            if names:
                if 1 < len(names) <= 3:
                    mail_list.append(f"{names[0].lower().strip()}.{names[-1].lower().strip()}@{self.domain}")
                    mail_list.append(f"{names[-1].lower().strip()}.{names[0].lower().strip()}@{self.domain}")
                    mail_list.append(f"{names[-1]}@{self.domain}")
                    mail_list.append(f"{names[0]}@{self.domain}")
                    mail_list.append(f"{names[0].lower().strip()}{names[-1].lower().strip()}@{self.domain}")
                    mail_list.append(f"{names[-1].lower().strip()}{names[0].lower().strip()}@{self.domain}")
                if len(names) == 3:
                    mail_list.append(
                        f"{names[0].lower().strip()}{names[1].lower().strip()}.{names[2].lower().strip()}@{self.domain}")
                    mail_list.append(
                        f"{names[0].lower().strip()}{names[1].lower().strip()}{names[2].lower().strip()}@{self.domain}")
                    mail_list.append(
                        f"{names[0].lower().strip()}.{names[1].lower().strip()}{names[2].lower().strip()}@{self.domain}")
                    mail_list.append(
                        f"{names[0].lower().strip()}.{names[2].lower().strip()}{names[1].lower().strip()}@{self.domain}")
        dic = {'email': mail_list, 'link': str(link), "mode": "permutated"}
        df = pd.DataFrame(dic)
        df.to_csv(self.path, mode='a', header=False)
        df.to_csv(self.path, mode='a', header=False)
        # print(mail_list, df)
