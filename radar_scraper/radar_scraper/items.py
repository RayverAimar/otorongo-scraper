# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RadarScraperItem(scrapy.Item):
    pass

class CandidateItem(scrapy.Item):
    name = scrapy.Field()
    dni = scrapy.Field()
    birth_date = scrapy.Field()
    home_address = scrapy.Field()
    birth_place = scrapy.Field()
    political_party = scrapy.Field()
    running_position = scrapy.Field()
    running_city = scrapy.Field()
    school_studies = scrapy.Field()
    technical_education = scrapy.Field()
    non_university_education = scrapy.Field()
    university_education = scrapy.Field()
    postgraduate_studies = scrapy.Field()
    other_postgraduate_studies = scrapy.Field()
    background_intentional_crimes = scrapy.Field()
    background_legal_confirmed = scrapy.Field()
    work_experience = scrapy.Field()
    additional_information = scrapy.Field()
    political_experience = scrapy.Field()
    party_history = scrapy.Field()
    year = scrapy.Field()