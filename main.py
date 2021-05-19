
from googlesearch import search
from scrapy.crawler import CrawlerProcess

from codes import CODES
from spider import MailSpider


def get_urls(query, n, language, country):
    if country not in CODES:
        print("Specify the correct country")
        return
    tld = CODES[country]
    print(country, tld)
    urls = [url for url in search(query, tld=f"co.{tld}", stop=n, lang=language)][:n]
    return urls


google_urls = get_urls('manager at google', 5, 'en', "Kenya")
# mail_list = re.findall(r'[\w-\._\+%]+@test\.com',text)
process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
process.crawl(MailSpider, start_urls=google_urls, path="new.csv", reject=[])
process.start()