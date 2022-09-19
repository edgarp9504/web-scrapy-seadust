import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree

# ow library
import aux_text

class ExpediaMX:
    
    def __init__(self):
        print('Extracción Expedia MX')
        
        self.header     = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}
        self.url        = "https://www.expedia.mx/Cancun-Hoteles-Seadust-Cancun-All-Inclusive-Family-Resort.h1579645.Informacion-Hotel"
        self.respuesta  = requests.get(self.url, headers = self.header)
        self.soup       = BeautifulSoup(self.respuesta.content, "html.parser")
        self.dom        = etree.HTML(str(self.soup))

        self.date       = time.strftime("%d/%m/%Y")
        
        self.extrac_info()
    
    
    def dowload_csv(self, data):
        print('Generando el CSV...') 
        df = pd.DataFrame(data = data)
        return df.to_csv(f'csv_file/seadust-expediaMX.csv',index = False, header=True)
    
    
    def extrac_info(self):
                

        dataset = {'nombre': [], 'conceptop': [], 'fecha_review' : [], 'critica' : [], 'review' : [], 'estadia' : [], 'date_extract' : []}
        
        list_reviews = self.dom.xpath('//div[@class="uitk-card-content-section uitk-card-content-section-border-block-end uitk-card-content-section-padded"]')

        for review_only in list_reviews:
            nombre       = review_only.xpath('.//span[@itemprop="name"]')[0].text
            conceptop    = review_only.xpath('.//div[@class="uitk-text uitk-type-300 uitk-text-default-theme"]')[0].text
            fecha_review = review_only.xpath('.//span[@itemprop="datePublished"]')[0].text
            critica      = review_only.xpath('.//span[@class="uitk-text uitk-type-200 uitk-spacing uitk-spacing-padding-inlinestart-two uitk-text-default-theme"]')[0].text
            review       = review_only.xpath('.//span[@itemprop="description"]')[0].text
            estadia      = review_only.xpath('.//div[@class="uitk-text uitk-type-200 uitk-layout-flex-item uitk-text-default-theme"]')[0].text
        
            review = aux_text.remove_newline(review)
            
            if conceptop is None:
                conceptop = 'Sin concepto'
        
            dataset['nombre'].append(nombre)
            dataset['conceptop'].append(conceptop)
            dataset['fecha_review'].append(fecha_review)
            dataset['critica'].append(critica)
            dataset['review'].append(review)
            dataset['estadia'].append(estadia)
            dataset['date_extract'].append(self.date)
        
        
        return self.dowload_csv(dataset)