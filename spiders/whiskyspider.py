import scrapy


class WhiskySpider(scrapy.Spider):
    name = "whisky"
    start_urls = ['https://www.whiskyshop.com/newreleases/new-scotch-whisky']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            try:
                yield {
                    'name': products.css('a.product-item-link::text').get() ,
                    'price': products.css('span.price::text').get().replace('£',''),
                    'link': products.css('a.product-item-link').attrib['href']
                }
            except:
                yield {
                    'name': products.css('a.product-item-link::text').get(),
                    'price': 'sold out',
                    'link': products.css('a.product-item-link').attrib['href']
                }
        #Dobi naslednjo stran ; v tem primeru je ni
        next_page = response.css('a.action.next').attrib['href']

        #ČE obstaja naslednja stran follow next page, če obstaja, pokliči funkcijo Parse
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
        

