# 140062D
# G.P.P.D Bandara
# IR Project [Data Mining and Information Retrieval]

import scrapy

class BlogSpider(scrapy.Spider):
    name = "news_articles"
    start_urls = ['http://www.hirunews.lk/all-news.php?pageID=1']
    count = 0
    result_count = 0

    def parse(self, response):
        for article_url in response.css('.lts-cntp a ::attr("href")').extract():
            yield response.follow(article_url, callback=self.parse_article)
            BlogSpider.result_count += 1
        older_posts = response.css('.pagi_2 a ::attr("href")').extract()

        if older_posts is not None:
            BlogSpider.count += 1
            # Previous button is changing depending on the page
            # Older post link is located in the 3rd element of the href array on the first page
            # it is located in the 5th element on reset of the pages
            if BlogSpider.count == 1:
                url = older_posts[2]
            else:
                url = older_posts[4]

            print('--------Redirected URL [For Older Posts]----------')
            print(older_posts)
            print('following: ' + url)
            print('--------------------------------------------------')
            yield response.follow(url, callback=self.parse)

    def parse_article(self, response):
        title = response.xpath(".//div[@class='lts-cntp2']/descendant::text()").extract()
        content = response.xpath(".//div[@class='lts-txt2']/descendant::text()").extract()
        time = response.xpath(".//div[@class='lts-cntbx2']/div[@class='time']/descendant::text()").extract()
        views_count = response.xpath(".//div[@class='sl_box3']/descendant::text()").extract()
        last_updated_date = response.xpath(".//div[@class='latest-time hidden-xs']/descendant::text()").extract()

        # Data Pre-Processing
        # article_content
        article_content = ''
        for input_content in content:
            input_content.encode("utf-8")
            # for check only valid informations
            is_valid_content = True
            if input_content == "\r\n" or input_content == "\xa0"\
                    or input_content == " " or input_content.find('\xa0') != -1:
                is_valid_content = False
            if is_valid_content:
                # in case of unicode encode error
                input_content.replace("\u2013", "-")
                input_content.replace("\xa0", " ")

                if article_content=='':
                    article_content = input_content
                else:
                    article_content += " " + input_content
        # title, time and view_count
        article_title = title[0]
        article_time = time[0]
        article_view_count = views_count[0]
        article_last_updated = last_updated_date[0]

        # display the output
        try:
            print('---------Scrap Data [' + str(BlogSpider.result_count) + ']---------')
            print(title)
            print(time)
            print(views_count)
            print(content)
            print(last_updated_date)
            print('-----Pre-Processed Data--------')
            print(article_title)
            print(article_time)
            print(article_view_count)
            print(article_content.encode("utf-8"))
            print(article_last_updated)
            print('-------------------------------')
        except UnicodeEncodeError:
            print('Error on printing results [UnicodeEncodeError]')

        # Write the data to the json
        yield {'title': ''.join(article_title), 'time': ''.join(article_time),
               'view_count': ''.join(article_view_count), 'last_updated_date': ''.join(article_last_updated),
               'content': ''.join(article_content)}
