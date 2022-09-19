import csv
import random
import pandas as pd
import time
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# ow library
import aux_text



class TripAdvisor():
    
    def __init__(self):
        print('Extracción de TripAdvisor')
        self.opts = Options()
        self.opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
        self.url = 'https://www.tripadvisor.com.mx/Hotel_Review-g150807-d634235-Reviews-Seadust_Cancun_Family_Resort-Cancun_Yucatan_Peninsula.html'
        self.driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=self.opts)

        self.date = time.strftime("%d/%m/%Y")
        
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
        
        return df.to_csv(f'csv_file/seadust-tripadvisor.csv',index = False, header=True)
    
    # def to_mysql(self):
        
    
    def extrac_info(self):
        sleep(random.uniform(4.0, 5.0))
        self.driver.execute_script("window.scrollTo(0, 1000)")

        #click comentarios
        self.click_button('xpath', '//div[@class="REVIEWS XhvNN d q _T _h W z xBgrj"]')

        # clic button radio
        self.click_button("xpath", '//li[@class="ui_radio XpoVm"]')
        

        sleep(random.uniform(2.0, 3.0))

        iteraccion_per_page = 1
        page_next = 1
        

        dataset = {'nombre': [], 'titulo': [], 'review' : [], 'estadia' : [], 'rating' : [],'date_extract' : []}

        
        ### Obteniendo los primeros reviews
        get_reviews = self.driver.find_elements("xpath", '//div[@class="YibKl MC R2 Gi z Z BB pBbQr"]')
        
        print('obteniendo la página..',1)
        for review in get_reviews: 
            user = review.find_element("xpath", './/div[@class="cRVSd"]/span/a').text
            title = review.find_element("xpath", './/div[@class="KgQgP MC _S b S6 H5 _a"]/a/span/span').text
            review_user = review.find_element("xpath", './/q[@class="QewHA H4 _a"]/span').text
            fecha_estadia = review.find_element("xpath", './/span[@class="teHYY _R Me S4 H3"]').text
            rating = review.find_element("xpath", './/div[@class="Hlmiy F1"]/span').get_attribute("class")
            
            rating = rating.split('_')[-1]
            
            # Delete Emoji
            review_user = aux_text.delete_emoji(review_user)
            

            dataset['nombre'].append(user)
            dataset['titulo'].append(title)
            dataset['review'].append(review_user)
            dataset['estadia'].append(fecha_estadia)
            dataset['rating'].append(rating)
            dataset['date_extract'].append(self.date)
            
        #Get all review in each page
        while (iteraccion_per_page != 3):
            sleep(random.uniform(2.0, 4.0))
            
            button_next_page = self.driver.find_element("xpath", f'//div[@class="pageNumbers"]/a[{page_next}]')
            button_next_page.click() 
            number_of_page = self.driver.find_element("xpath", '//span[@class="pageNum current disabled"]').text
            print('obteniendo la página..',number_of_page)
            
            sleep(random.uniform(2.0, 4.0))
            get_reviews = self.driver.find_elements("xpath", '//div[@class="YibKl MC R2 Gi z Z BB pBbQr"]')
            for review in get_reviews:
                user = review.find_element("xpath", './/div[@class="cRVSd"]/span/a').text
                title = review.find_element("xpath", './/div[@class="KgQgP MC _S b S6 H5 _a"]/a/span/span').text
                review_user = review.find_element("xpath", './/q[@class="QewHA H4 _a"]/span').text
                fecha_estadia = review.find_element("xpath", './/span[@class="teHYY _R Me S4 H3"]').text
                rating = review.find_element("xpath", './/div[@class="Hlmiy F1"]/span').get_attribute("class")
                
                review_user = aux_text.delete_emoji(review_user)
                rating = rating.split('_')[-1]
                
                dataset['nombre'].append(user)
                dataset['titulo'].append(title)
                dataset['review'].append(review_user)
                dataset['estadia'].append(fecha_estadia)
                dataset['rating'].append(rating)
                dataset['date_extract'].append(self.date)            

            iteraccion_per_page+=1
            if int(number_of_page) >= 5:
                page_next = 4
            else:
                page_next+=1
        
        
        return self.dowload_csv(dataset)
        

