import socket
import sys
import urllib

import pandas as pd
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QWidget, QApplication
from googlesearch import search
from scrapy.crawler import CrawlerProcess
from twisted._threads import ThreadWorker

from codes import CODES
from spider import MailSpider


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.threadpool = QThreadPool()
        self.extract()

    def get_urls(self,query, n, language, country):
        if country not in CODES:
            print("Specify the correct country")
            return
        tld = CODES[country]
        print(country, tld)
        print("Getting the urls...")

        try:
            urls = [url for url in search(query, tld=f"co.{tld}", stop=n, lang=language)][:n]
        except (socket.gaierror, urllib.error.URLError):
            urls = [url for url in search(query, tld=f"com", stop=n, lang=language)][:n]
        return urls

    def extract(self):
        path = "new.csv"
        df = pd.DataFrame(columns=['email', 'link'], index=[0])
        df.to_csv(path, mode='w', header=True)

        google_urls = self.get_urls('manager at a company', 3, 'en', "United States of America")
        # mail_list = re.findall(r'[\w-\._\+%]+@test\.com',text)
        process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
        bad = ["twitter", "facebook", "instagram", "google"]
        process.crawl(MailSpider, start_urls=google_urls, path=path, reject=bad)
        process.start()
        worker = ThreadWorker(process.start)

        self.threadpool.start(worker)



def main():
    app = QApplication(sys.argv)
    MainWindow()
    # window = Password_ui()
    # window.show()
    app.exec_()


if __name__ == '__main__':
    main()