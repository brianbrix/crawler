import pandas as pd
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
    print("Getting the urls...")
    urls = [url for url in search(query, tld=f"co.{tld}", stop=n, lang=language)][:n]
    return urls


path = "new.csv"
df = pd.DataFrame(columns=['email', 'link'], index=[0])
df.to_csv(path, mode='w', header=True)

google_urls = get_urls('manager at google', 1, 'en', "Kenya")
# mail_list = re.findall(r'[\w-\._\+%]+@test\.com',text)
process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0'})
process.crawl(MailSpider, start_urls=google_urls, path=path, reject=[])
process.start()

print('Cleaning the save file...')
df = pd.read_csv(path, index_col=0)
df.columns = ['email', 'link']
df = df.drop_duplicates(subset='email')
df = df.reset_index(drop=True)
df.to_csv(path, mode='w', header=True)
