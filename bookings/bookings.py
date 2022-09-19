import random
import pandas as pd
import time
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

# ow library
import aux_text


class Booking:
    
    def __init__(self):
        self.opts   = Options()
        self.opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
        self.url    = 'https://www.booking.com/hotel/mx/great-parnassus-resort-spa.es-mx.html#tab-reviews'
        self.driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=self.opts)
                

        self.date       = time.strftime("%d/%m/%Y")
        
        
        self.getUrl()
        self.extrac_info()
    
    
    def getUrl(self):
        self.driver.get(self.url)
        
    def click_button(self, tipe, dom):
        sleep(random.uniform(2.0, 3.0))
        button = self.driver.find_element(tipe, dom)
        return button.click()
    

    def dowload_csv(self, data):
        print('Generando el CSV...')  
        df = pd.DataFrame(data = data)
        return df.to_csv(f'csv_file/seadust-booking.csv',index = False, header=True)
    
        
    def extrac_info(self):
        sleep(random.uniform(4.0, 5.0))
        self.driver.execute_script("window.scrollTo(0, 1000)")
        
        dataset = {'nombre': [], 'titulo': [], 'review_good' : [], 'review' : [],'Fecha_comentario' : [], 'rating' : [], 'date_extract': []}

        # Get the firts reviews
        sleep(random.uniform(4.0, 5.0))
        reviews = self.driver.find_elements("xpath", '//ul[@class="review_list"]//div[@class="c-review-block"]')            
        
        print('obteniendo datos de la página.....1')
        for review in reviews:
            sleep(random.uniform(1.0, 2.0))
                
            nombre           = review.find_element("xpath", './/span[@class="bui-avatar-block__title"]').text
            Fecha_comentario = review.find_element("xpath", './/div[@class="c-review-block__row"]/span').text
            rating           = review.find_element("xpath", './/div[@class="bui-review-score__badge"]').text
            titulo           = review.find_element("xpath", './/h3').text
            review_good      = review.find_element("xpath", './/p[@class="c-review__inner c-review__inner--ltr"]/span[@class="c-review__body"]').text
                       
            try:
                review   = review.find_element("xpath", './/div[@class="c-review__row lalala"]//span[@class="c-review__body"]').text
            except NoSuchElementException:
                review   = 'sin comentario'
                
            # Delete Emoji
            review_good = aux_text.delete_emoji(review_good)
            review = aux_text.delete_emoji(review)

            dataset['nombre'].append(nombre)
            dataset['Fecha_comentario'].append(Fecha_comentario)
            dataset['rating'].append(rating)
            dataset['titulo'].append(titulo)
            dataset['review_good'].append(review_good.rstrip())
            dataset['review'].append(review.rstrip())
            dataset['date_extract'].append(self.date)
        
        sleep(random.uniform(4.0, 5.0))

        
        #Get all reviews
        page_visit = 1        
        while page_visit !=3:
            page_visit += 1
            print('obteniendo datos de la página.....', page_visit)
            
            # Click to next page
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located(("xpath", '//div[@class="bui-pagination__item bui-pagination__next-arrow"]'))   
            ).click()
            
            sleep(random.uniform(2.0, 3.0))
            
            reviews = self.driver.find_elements("xpath", '//ul[@class="review_list"]//div[@class="c-review-block"]')            
            for review in reviews:
                sleep(random.uniform(1.0, 2.0))
                
                nombre           = review.find_element("xpath", './/span[@class="bui-avatar-block__title"]').text
                Fecha_comentario = review.find_element("xpath", './/div[@class="c-review-block__row"]/span').text
                rating           = review.find_element("xpath", './/div[@class="bui-review-score__badge"]').text
                titulo           = review.find_element("xpath", './/h3').text
                
                try:
                    review_good  = review.find_element("xpath", './/p[@class="c-review__inner c-review__inner--ltr"]/span[@class="c-review__body"]').text
                except NoSuchElementException:
                    review_good  = 'sin comentario'  
                                  
                try:
                    review   = review.find_element("xpath", './/div[@class="c-review__row lalala"]//span[@class="c-review__body"]').text
                except NoSuchElementException:
                    review   = 'sin comentario'
                    
                review_good = aux_text.remove_newline(review_good)
                review = aux_text.remove_newline(review)

                dataset['nombre'].append(nombre)
                dataset['Fecha_comentario'].append(Fecha_comentario)
                dataset['rating'].append(rating)
                dataset['titulo'].append(titulo)
                dataset['review_good'].append(review_good)
                dataset['review'].append(review)
                dataset['date_extract'].append(self.date)


        return self.dowload_csv(dataset)
        

