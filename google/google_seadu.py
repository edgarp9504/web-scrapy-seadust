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


class Google():
    
    def __init__(self):
        print('Extración de google...')
        self.opts = Options()
        self.opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
        self.url = 'https://www.google.com/maps/place/Seadust+Cancun+Family+Resort/@21.0685949,-86.7795631,17z/data=!4m10!3m9!1s0x8f4c282b8b5bad75:0xdb62aeba3cda5d8c!5m2!4m1!1i2!8m2!3d21.0685949!4d-86.7773744!9m1!1b1'
        self.driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=self.opts)
        self.date = time.strftime("%d/%m/%Y")
        
        self.getUrl()
        self.extrac_info()
    
    
    def getUrl(self):
        self.driver.get(self.url)
        
    def click_button(self, tipe, dom):
        """Function to click a event

        Args:
            tipe (_type_): XPATH
            dom (_type_): DOM

        Returns:
            _type_: Return the event click
        """
        sleep(random.uniform(2.0, 3.0))
        button = self.driver.find_element(tipe, dom)
        return button.click()

    def dowload_csv(self, data):
        print('Generando el CSV...')  
        df = pd.DataFrame(data = data)
        return df.to_csv(f'csv_file/seadust-google.csv',index = False, header=True)
        
    def extrac_info(self):
        sleep(random.uniform(4.0, 5.0))

        self.click_button("xpath", '//div[@class="m6QErb Hk4XGb tLjsW"]/button[2]')
        self.click_button("xpath", '//div[@id="action-menu"]/ul/li[2]')
        sleep(random.uniform(2.0, 3.0))


        # SCRIIPTS JAVASCRIPT
        scrollingScroll = """
                            document.getElementsByClassName('m6QErb DxyBCb kA9KIf dS8AEf')[0].scroll(0, 20000)
                            """

        SCROLLS = 0

        ## Hace el scroll
        while(SCROLLS != 3):
            self.driver.execute_script(scrollingScroll)
            sleep(random.uniform(5, 6))
            SCROLLS +=1

        #Creando de DataFrame
        dataset = {'nombre': [], 'ranking': [], 'fecha' : [], 'review' : [],'date_extract' : []}


        # Encontrando cada review y generarlo en una lista
        reviews_restaurante = self.driver.find_elements("xpath", '//div[@class="jftiEf fontBodyMedium"]')
        print('Elementos encontrados..')

        #loop para entrar en cada usuario que hizo un review
        for review in reviews_restaurante:
            try:
                nombre  = review.find_element("xpath", './/div[@class="d4r55"]/span').text
                ranking = review.find_element("xpath", './/span[@class="fzvQIb"]').text
                fecha   = review.find_element("xpath", './/span[@class="xRkPPb"]/span').text
                review  = review.find_element("xpath", './/div[@class="MyEned"]/span[2]').text
                
                if not review:
                    review = 'sin comentario' 
                
                # Delete Emoji
                review = aux_text.delete_emoji(review)
                
                dataset['nombre'].append(nombre)
                dataset['ranking'].append(ranking)
                dataset['fecha'].append(fecha)
                dataset['review'].append(review)
                dataset['date_extract'].append(self.date)
               
                
            except Exception as e:
                print(e)
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
        
        return self.dowload_csv(dataset)
        

