import socket
import sys
import urllib

import pandas as pd
from PyQt5 import Qt
from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QListView, QCompleter, QComboBox, \
    QFileDialog
from googlesearch import search
from scrapy.crawler import CrawlerProcess

from codes import CODES, CustomQCompleter
from spider import MailSpider
from thread_func import ThreadWorker
import scrapy
import google

emails = set()

from interface import Ui_MainWindow as ui


class Main_ui(QMainWindow, ui):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)


class MainWindow(Main_ui):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.threadpool = QThreadPool()
        # self.extract()
        self.addCountries()
        self.pushButton.clicked.connect(self.extract)

    def addCountries(self):
        AllItems = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
        self.comboBox.addItems(
            sorted(set([x for x in [k for k in CODES] if x not in AllItems and x is not None]))
        )
        model = QStandardItemModel()
        for item in CODES:
            it = QStandardItem(item)
            model.appendRow(it)
        view = QListView()
        view.setUniformItemSizes(True)
        view.setLayoutMode(QListView.Batched)
        self.comboBox.setView(view)
        self.comboBox.setEditable(True)
        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.comboBox.setModel(model)

        # if editable:
        completer = CustomQCompleter(self.comboBox)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setModel(self.comboBox.model())
        completer.setCaseSensitivity(Qt.Qt.CaseInsensitive)
        completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.comboBox.setCompleter(completer)

    def get_urls(self, query, n, language, country):
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
        """

        :return:
        """
        self.key = self.search_key.text()
        self.country = self.comboBox.currentText()
        self.num_results = self.spinBox.text()
        if any(x == "" for x in [self.key, self.country, self.num_results]) or int(self.num_results) <= 0:
            QMessageBox.critical(self, "Error",
                                 "Make sure you have filled the search key, country and number of results")
            return
        path2 = QFileDialog.getSaveFileName(self, "Select csv file to save fina result.", '.', '.csv')[0]
        if path2:
            path = "new.csv"
            df = pd.DataFrame(columns=['email', 'link', "mode"], index=[0])
            df.to_csv(path, mode='w', header=True)
            # path2 = "validate.csv"
            df = pd.DataFrame(columns=['email', 'firstname', "lastname", "mode"], index=[0])
            df.to_csv(path2, mode='w', header=True)

            google_urls = self.get_urls(self.key, int(self.num_results), 'en', self.country)
            process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
            bad = ["twitter", "facebook", "instagram", "google", "linkedin", "pinterest"]
            process.crawl(MailSpider, start_urls=google_urls, path=path, path2=path2, reject=bad, res_emails=emails)
            process.start()
        else:
            QMessageBox.critical(self, "Error",
                                 "Please select a file to continue.")
            return


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    # window = Password_ui()
    # window.show()
    app.exec_()


if __name__ == '__main__':
    main()
