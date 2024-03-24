import scrapy

class TherapistsSpider(scrapy.Spider):
    name = 'therapists'
    allowed_domains = ['psychologytoday.com']
    start_urls = [f'https://www.psychologytoday.com/us/therapists/ny/brooklyn?page={i}' for i in range(1, 278)]

    def parse(self, response):
        for therapist in response.css('div.results-row.top-divider'):
            yield {
                'name': therapist.css('a.profile-title::text').get(),
                'title': therapist.css('div.profile-subtitle-credentials::text').get(),
                'address': therapist.css('span.address::text').getall(),
                'phone': therapist.css('span.results-row-phone::text').get(),
                'statement': therapist.css('div.statements::text').get(),
                'image': therapist.css('img.image::attr(src)').get(),
                'profile_url': therapist.css('a.profile-title::attr(href)').get(),
            }
