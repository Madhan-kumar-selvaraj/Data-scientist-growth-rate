from .ds_growth_db import insert_data  # Impoting insert_data function to load data into database
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "dsgrowth"   # Spider name
    minimum_experience = 'NA'  # Default value if there is no value while scraping
    maximum_experience = 'NA'
    next_page = []
    # Body data for the POST method
    body_data = "qp=data+scientist&ql=bangalore&qe=&qm=&qx=&qi%5B%5D=&qf%5B%5D=&qr%5B%5D=&qs=r&qo=&qjt%5B%5D=&qk%5B%5D=&qwdt=&qsb_section=home&qpremTagLabel=&sid=15810530081808&qwd%5B%5D=&qcf%5B%5D=&qci%5B%5D=&qck%5B%5D=&edu%5B%5D=&qcug%5B%5D=&qcpg%5B%5D=&qctc%5B%5D=&qco%5B%5D=&qcjt%5B%5D=&qcr%5B%5D=&qctags%5B%5D=&qcl%5B%5D=&qrefresh=&xt=adv&qtc%5B%5D=&fpsubmiturl=https%3A%2F%2Fwww.naukri.com%2Fdata-scientist-jobs-in-bangalore&qlcl%5B%5D=&latLong="
    
    # Our program starts in this function
    def start_requests(self):
        url = "https://www.naukri.com/data-scientist-jobs" # Main URL
        yield scrapy.Request(url=url, method='POST',body=self.body_data, callback= self.parse)

    def parse(self, response):
        # To handle exceptions
        try:
            dict_data = {'key_data': []}  # Used to load data into database effectively
            for row_data in response.css('div.row  '):  # To extract all the jobs from a page
                designation = row_data.xpath('.//li[@class="desig"]//text()').extract_first()
                if designation is not None:  # Checking the value
                    company = row_data.xpath('.//span[@class="org"]/text()').extract_first()
                    salary = row_data.xpath('.//span[@class="salary"]//text()').extract_first()
                    skill = row_data.xpath('//span[@class="skill"]//text()').extract_first()
                    posted_on = row_data.xpath('.//span[@class="date"]//text()').extract_first()
                    experience = row_data.xpath('.//span[@class="exp"]//text()').extract_first()
                    location = row_data.xpath('.//span[@class="loc"]//text()').extract_first()
                    salary = "NAN" if (salary.strip() == "Not disclosed" or salary.strip() == "") else salary.strip()
                    # Splitting experience value into min and max
                    # Strip used to remove the unwanted spaces
                    if experience is not None:
                        split_result = experience.strip('yrs').split('-') if "-" in experience else experience
                        if len(split_result) > 1:
                            self.minimum_experience = (split_result[0]).strip()
                            self.maximum_experience = (split_result[1]).strip()
                    extracted_data =(designation.strip(), company.strip(), skill.strip(), salary.strip(), posted_on.strip(), location.strip(), self.minimum_experience, self.maximum_experience)
                    # To convert values into list of tuples
                    dict_data['key_data'].extend([extracted_data])
            # Insert the extracted data into the database
            insert_data(dict_data['key_data'])
            self.next_page = response.xpath('//div[@class="pagination"]/a//@href').extract()
            self. next_page = self. next_page[-1]
            
            
            # Iterate to the next page to scrape the data
            if self.next_page is not None:
                yield scrapy.Request(self.next_page,  method='POST',body=self.body_data, callback=self.parse)


        except Exception as e:
            print(e)

