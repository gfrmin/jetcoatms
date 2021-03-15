import xml.etree.ElementTree as ET

import scrapy


class JetcoatmsSpider(scrapy.Spider):
    name = 'jetcoatms'
    allowed_domains = ['jetco.com.hk']
    areaids = [1,2,3,4,23]
    start_urls = ['https://www.jetco.com.hk/xml/en/atm/{}_atmDistrict.xml'.format(areaid) for areaid in areaids]

    def parse(self, response):
        root = ET.fromstring(response.text)
        for districts in root:
            for district in districts:
                areaid = districts.attrib.get('area_id')
                if int(areaid) < 10:
                    countryid = 2
                else:
                    countryid = 3
                yield scrapy.Request('https://www.jetco.com.hk/xml/en/atm/{}_{}_{}_0_atmDetails.xml?timestamp=1615738056969'.format(countryid, areaid, district.find('district_id').text), callback = self.parse_atms)
                                        
    def parse_atms(self, response):
        root = ET.fromstring(response.text)
        atms = root[1]
        for atm in atms:
            atmdict = {
                'latitude': float(atm.find('latitude').text) if atm.find('latitude').text else None,
                'longitude': float(atm.find('longitude').text) if atm.find('longitude').text else None,
                'bank': atm.find('ob_name').text,
                'address': atm.find('addr').text,
                'tran': [t.text for t in atm.iter('tran_name')],
                'currencies': [t.text for t in atm.iter('currency')]
            }
            yield atmdict
