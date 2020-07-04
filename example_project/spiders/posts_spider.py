import scrapy

from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
# from example_project.example_project.items import Posts
from example_project.items import Posts

MAX_PAGES = 15


class PostsSpiderBackward(scrapy.Spider):
    name = "posts"

    def start_requests(self):
        for page_index in range(MAX_PAGES):
            yield scrapy.Request(url=f'https://news.ycombinator.com/news?p={page_index}', callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        soup = BeautifulSoup(response.body)
        a_list = soup.findAll("a")
        for i in a_list:
            if i.attrs.get('class') == ['storylink']:
                loader = ItemLoader(item=Posts(), response=response)
                loader.add_value('url', i.attrs.get('href'))
                loader.add_value('title', i.text.replace('\'', '"'))
                yield loader.load_item()


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PostsSpiderBackward)
    process.start()
