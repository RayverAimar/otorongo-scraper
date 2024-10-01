from typing import Iterable
import scrapy

from radar_scraper.items import CandidateItem

class OtorongoSpider(scrapy.Spider):
    name = "otorongo"
    allowed_domains = ["otorongo.club"]
    start_urls = ["https://otorongo.club/2021/sentencias/",
                  "https://otorongo.club/2022/sentencias/"]

    custom_settings = {
        'FEEDS':
            {
                'candidates_otorongo.json' :
                    {
                        'format' : 'json',
                        'overwrite' : True,
                    }
            }
    }

    def start_requests(self):
        for url in self.start_urls:
            year = url.split('/')[3]
            yield scrapy.Request(url, callback=self.parse, meta={'year': year})

    def parse(self, response):
        year = response.meta['year']
        
        candidates = response.css('tr')[1:]
        
        for candidate in candidates:
            candidate_page_url = candidate.css('td')[2].css('a::attr(href)').get()
            yield response.follow(url=candidate_page_url,
                                  callback=self.parse_candidate,
                                  meta={'year': year}
                                  )
        
        next_page_url = response.css('div.text-center li')[-1].css('a::attr(href)').get()
        
        if next_page_url:
            yield response.follow(url=next_page_url,
                                  callback=self.parse,
                                  meta={'year':year}
                                  )

    def parse_candidate(self, response):
        year = response.meta['year']
                
        name = response.css('h3.text-white::text').get()
        dni = response.css('li.list-inline-item')[0].css('h5::text').get()
        birth_date = response.css('li.list-inline-item')[1].css('h5::text').get()
        
        manolo = 1 if 'Manolo' in response.css('div.content > div')[3].css('h4.header-title::text').get() else 0
        supposed_plan_block = response.css('div.content > div')[4].css('h4.header-title i').xpath('following-sibling::text()').get()
        plan = 0
        if supposed_plan_block and 'Plan de Gobierno' in supposed_plan_block:
            plan = 1
        
        personal_info = response.css('p.text-muted')
        
        home_address = personal_info[0].css('span::text').get()
        birth_place = personal_info[1].css('span.ms-2::text').getall()
        political_party = personal_info[2].css('span::text').get()
        running_position = personal_info[3].css('::text')[1].get()
        running_city = personal_info[4].css('span::text').get()
        
        school_studies = response.css('div.card.d-none.d-sm-block li::text').getall()
        
        education = response.css('div.col-xl-8 > div')[0].css('li')[0].css('p::text').get()
        technical_education = education if education else '-'
        
        education = response.css('div.col-xl-8 > div')[0].css('li')[1].css('p::text').get()
        non_university_education = education if education else '-'
        
        university_education = response.css('div.col-xl-8 > div')[1].css('li::text').getall()
        
        postgraduate_studies = response.css('div.col-xl-8 > div')[2].css('li::text').getall()
        
        other_postgraduate_studies = response.css('div.col-xl-8 > div')[3].css('li::text').getall()
        
        ## See if candidates have more than one degree in technical
        ## and non_technical studies in order to scrape them all
        
        background_intentional_crimes_keys = response.css('table.table')[0].css('thead th::text').getall()
        background_intentional_crimes = []
        rows_intentional_crimes = response.css('table.table')[0].css('tbody tr')
        
        for row in rows_intentional_crimes:
            data = row.css('td::text').getall()
            background_intentional_crimes.append(dict(zip(background_intentional_crimes_keys, data)))
        
        background_legal_confirmed_keys = response.css('table.table')[1].css('thead th::text').getall()
        background_legal_confirmed = []
        rows_background_legal_confirmed = response.css('table.table')[1].css('tbody tr')
        
        for row in rows_background_legal_confirmed:
            data = row.css('td::text').getall()
            background_legal_confirmed.append(dict(zip(background_legal_confirmed_keys, data)))
        
        work_experience = []
        
        # This changes behavior depending if the candidate has a documented plan or is identified in Manolo
        jobs = response.css('div.content > div')[6 + manolo + plan].css('li')
        
        for job in jobs:
            time_lapse = job.css('strong::text').get()
            info = job.css('br').xpath('following-sibling::text()').get()
            work_experience.append({'time_lapse': time_lapse,
                                    'info': info})
        
        additional_information = response.css('div.row')[-1].css('div.card')[4].css('li::text').get()
        additional_information = additional_information if additional_information else '-'
        
        political_experience = []
        
        parties = response.css('div.row')[-1].css('div.card')[5].css('li')
        
        for party in parties:
            time_lapse = party.css('strong::text').get()
            info = party.css('br').xpath('following-sibling::text()').get().strip()
            political_experience.append({'time_lapse': time_lapse,
                                            'info': info})
        
        party_history = []
        parties = response.css('div.row')[-1].css('div.card')[6].css('li')
        
        for party in parties:
            time_lapse = party.css('strong::text').get()
            info = party.css('br').xpath('following-sibling::text()').get().strip()
            party_history.append({'time_lapse': time_lapse,
                                  'info': info})
        
        candidate = CandidateItem()
        
        candidate['name'] = name
        candidate['dni'] = dni
        candidate['birth_date'] = birth_date
        candidate['home_address'] = home_address
        candidate['birth_place'] = birth_place
        candidate['political_party'] = political_party
        candidate['running_position'] = running_position
        candidate['running_city'] = running_city
        candidate['school_studies'] = school_studies
        candidate['technical_education'] = technical_education
        candidate['non_university_education'] = non_university_education
        candidate['university_education'] = university_education
        candidate['postgraduate_studies'] = postgraduate_studies
        candidate['other_postgraduate_studies'] = other_postgraduate_studies
        candidate['background_intentional_crimes'] = background_intentional_crimes
        candidate['background_legal_confirmed'] = background_legal_confirmed
        candidate['work_experience'] = work_experience
        candidate['additional_information'] = additional_information
        candidate['political_experience'] = political_experience
        candidate['party_history'] = party_history
        candidate['year'] = year

        return candidate