import scrapy


class BrokerspiderSpider(scrapy.Spider):
    name = "brokerspider"
    allowed_domains = ["brokersireland.ie"]
    start_urls = ["https://brokersireland.ie/broker/"]

    def parse(self, response):
        companies_block = response.xpath('//div[@class="part-pan"]')
        for company in companies_block:
            company_url = company.xpath('.//div[@class="details"]/div/a/@href').get()
            yield response.follow(company_url, callback=self.parse_company)

        for next_page in range(2, 67):
            next_page_url = f'https://brokersireland.ie/broker/page/{next_page}/'
            yield response.follow(next_page_url, self.parse)

    def parse_company(url, response):
        name = response.xpath('//div[@class="broker-spec"]/div/table//tr[1]/td[2]/text()').get()
        location = response.xpath('//div[@class="broker-spec"]/div/table//tr[2]/td[2]/text()').get(default = "NOT AVAILABLE")
        phone = response.xpath('//div[@class="broker-spec"]/div/table//tr[3]/td[2]/text()').get(default = "NOT AVAILABLE")
        email = response.xpath('//div[@class="broker-spec"]/div/table//tr[4]/td[2]/text()').get(default = "NOT AVAILABLE")
        website =response.xpath('//div[@class="broker-spec"]/div/table//tr[5]/td[2]/a/text()').get(default = "NOT AVAILABLE")
        yield{
            "Company_name" : name,
            "Company_Location" : location,
            "Phone" : phone,
            "Email" : email,
            "Website" : website,
        }       
