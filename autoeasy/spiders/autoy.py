from ast import Yield
from xml.etree.ElementTree import C14NWriterTarget
import scrapy
import urllib.parse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

 
 #file:///Users/souefhaitham/Desktop/test1/page.html

class AutoySpider(scrapy.Spider):
    name = 'autoy'
    #allowed_domains = ['https://www.autoeasy.fr/acheter']
    start_urls = ['https://www.autoeasy.fr/acheter?p='+str(k) for k in range(1,18)]
    
    #dic_critere = dict() 

    def parse(self, response):
        for link in response.xpath("//a[@class='product-name']/@href"):
            yield response.follow(link.get(), callback=self.parse_categories)
            #time.sleep(10)

    #def add_dic_critere(self,dic_critere):

    def parse_categories(self,response):
        
        def suprimer_espace_debut_fin(c) :
            if c[0]==' ' :
                c = c[1:]
            if c[-1]==' ':
                c = c[:-1]
            return c
        
        dic = { 'Nom'  : response.xpath("//h1[@class='name']/text()").extract()[0].replace('\r\n\t\t\t\t\t\t\t\t','').replace('\r\n\t\t\t\t\t\t\t',''),
                'Marque' : response.xpath("//span[@itemprop='name']/text()").extract()[2].replace('occasion','').replace(' ',''),
                'Modèle' : response.xpath("//span[@itemprop='name']/text()").extract()[3],
        }

               
        for cle, valeur in zip(response.xpath("//div[@class='col-4']/p[1]/text()").extract(),response.xpath("//div[@class='col-4']/p[2]/text()").extract()):
            if cle == 'Mise en circulation':
                dic.update({cle : valeur.replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','').replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','')})
            elif cle == 'Puissance fiscale':
                if (valeur.replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','').replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','').replace('Ch','') == 'N.C'):
                    next
                else :
                    dic.update({cle : valeur.replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','').replace('\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t','').replace('Ch','')})
            elif (cle == 'Garantie') :
                next 
            elif cle == 'Prix':
                dic.update({cle : valeur.replace('€','').replace(' ','')})
            elif cle == 'Emission de CO2':
                dic.update({cle : valeur.replace('g/km','')})
            elif cle=='Modèle':
                dic.update({cle : suprimer_espace_debut_fin(valeur)})
            elif cle == 'Kilométrage':
                dic.update({cle : valeur.replace('km','')})
            else:
                dic.update({cle : valeur})

        raw_image_urls = response.xpath("//img[@id='bigpic']/@src").extract()
        clean_images_urls = []
        for img_url in raw_image_urls :
            if img_url == "https://www.autoeasy.fr/img/p/fr-default-thickbox_default.jpg":
                clean_images_urls.append("https://www.countryobchod.cz/__files/web/obrazky/system/no-image.jpg")
            elif img_url == 'https://www.autoeasy.fr/img/p/vehicule_vendu.jpg':
                clean_images_urls.append("https://www.countryobchod.cz/__files/web/obrazky/system/no-image.jpg")
            else:
                clean_images_urls.append(response.urljoin(img_url))

        dic.update({'image_urls': clean_images_urls})
       
        yield dic
    
