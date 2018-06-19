import scrapy
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = "general"
    count = 0

    allowed_domains = ["hirunews.lk"]
    start_urls = ['http://www.hirunews.lk/']

    def parse(self, response):
        body = response.body
        soup = BeautifulSoup(body)

        # To display the count
        self.count = self.count + 1
        print ("********************* %d ************************"%(self.count))

        # Saving the page
        name = response.url
        name = name.replace("/", "-")
        name = name.replace("?", "")
        name = name.replace(".", "-")
        name = name.replace("http:--", "")

        # Create a filename
        filename = 'data/data-%s.html' % name
        with open(filename, 'wb') as f:
            # write the content to the file
            f.write(body)
        self.log('Saved file %s' % filename)

        # Extracting links
        links = soup.find_all('a')
        for link in links:
            next_route = link.get('href')
            yield response.follow(next_route, callback=self.parse)
