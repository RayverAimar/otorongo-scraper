# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class RadarScraperPipeline:
    def process_item(self, item, spider):
        return item

class OtorongoSpiderPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        ## Strip, delete newlines and spaces between words
        keys_to_strip = ['name', 'dni', 'birth_date', 'home_address', 'political_party',
                         'running_position', 'running_city', 'technical_education',
                         'non_university_education', 'additional_information'
                         ]
        for key_to_strip in keys_to_strip:
            value = adapter.get(key_to_strip)
            adapter[key_to_strip] = ' '.join(value.split())


        ## UniversityEducation & postgraduate_studies & other_postgraduate_studies --> Format arrays
        keys_to_format = ['university_education', 'postgraduate_studies', 'other_postgraduate_studies']
        for key in keys_to_format:
            values = adapter.get(key)
            formatted_values = [' '.join(value.split()) for value in values]
            adapter[key] = formatted_values
        
        
        ## BirthPlace --> Get array into one string, strip and delete spaces between words
        birth_place_array_string = adapter.get('birth_place')
        birth_place_array_string = ' '.join(birth_place_array_string).split()
        if birth_place_array_string[1] == 'PERÚ':
            birth_place = ', '.join([birth_place_array_string[1], birth_place_array_string[3],
                                    birth_place_array_string[5], birth_place_array_string[7]]
                                    )
        else:
            birth_place = birth_place_array_string[1]
        adapter['birth_place'] = birth_place
        
        
        ## WorkExperience & Political Experience --> Strip time_lapse and info 
        keys_to_format = ['work_experience', 'political_experience']
        for key in keys_to_format:
            values = adapter.get(key)
            if not values:
                continue
            formatted_values = [{'time_lapse':' '.join(value['time_lapse'].split()),
                                 'info':' '.join(value['info'].split())}
                                for value in values ]
            adapter[key] = formatted_values
        
        
        ## Only Capital Letters (useful?)
        
        return item