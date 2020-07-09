import scrapy
import datetime

from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
# from scrapy-example.scrapy-example.items import Posts
from scrapy_example.items import Posts
# from items import Posts

MAX_PAGES = 35
DATE_FORMAT = '%Y-%m-%d'
DEPTH_DAYS = 10


class PostsSpiderBackward(scrapy.Spider):
    name = "backward"
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 4.5
    }

    def start_requests(self):
        today = datetime.date.today()

        for day_number in range(1, DEPTH_DAYS):
            posts_day_dt = today - datetime.timedelta(days=day_number)
            posts_day_str = posts_day_dt.strftime(DATE_FORMAT)

            for page_index in range(1, MAX_PAGES):
                base_with_day_query = f'https://news.ycombinator.com/front?day={posts_day_str}&p='
                yield scrapy.Request(
                    url=f'{base_with_day_query}{page_index}',
                    callback=self.parse,
                    # headers={"User-Agent": "My UserAgent"},
                    # meta={"proxy": "http://127.0.0.1:9050"}
                )

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        a_list = soup.findAll("a")
        counter = 0
        for i in a_list:
            if i.attrs.get('class') == ['storylink']:
                title = i.text.replace('\'', '"')
                url = i.attrs.get('href')
                loader = ItemLoader(item=Posts(), response=response)
                loader.add_value('url', url)
                loader.add_value('title', title)
                self.log(f'Saved post url: {url} - title: {title}')
                yield loader.load_item()
            else:
                counter += 1


class PostsSpiderForward(scrapy.Spider):
    name = "forward"
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 4.5
    }

    def start_requests(self):
        url = 'https://news.ycombinator.com/news?p=1'
        yield scrapy.Request(url=f'{url}', callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        a_list = soup.findAll("a")
        counter = 0
        for i in a_list:
            if i.attrs.get('class') == ['storylink']:
                title = i.text.replace('\'', '"')
                url = i.attrs.get('href')
                loader = ItemLoader(item=Posts(), response=response)
                loader.add_value('url', url)
                loader.add_value('title', title)
                self.log(f'Saved post url: {url} - title: {title}')
                yield loader.load_item()
            else:
                counter += 1
        return response


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PostsSpiderForward)
    # process.crawl(PostsSpiderBackward)
    process.start()
