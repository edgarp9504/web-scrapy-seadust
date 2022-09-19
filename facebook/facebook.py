import pandas as pd
import time
from time import sleep
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# ow library
import aux_text


class Facebook:
    
    def __init__(self):
        print('Extracción de FB')
        self.opts       = Options()
        self.driver     = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=self.opts)
        self.driver.get("http://www.facebook.com")
        
        self.date       = time.strftime("%d/%m/%Y")
        
        self.extract_info()
        
    def login(self):
        username = self.driver.find_element("xpath",'//input[@name="email"]')
        password = self.driver.find_element("xpath",'//input[@id="pass"]')
        
        username.send_keys("9983253195")
        password.send_keys("Seadust.01")
        
        self.driver.find_element("xpath", '//button[@name="login"]').click()

    def dowload_csv(self, data):
        print('Generando el CSV...')  
        df = pd.DataFrame(data = data)
        return df.to_csv(f'csv_file/seadust-facebook.csv',index = False, header=True)
        
    
    def extract_info(self):

        self.login()
        
        sleep(random.uniform(4.0, 5.0))
        self.driver.get('https://www.facebook.com/SeadustCancun/reviews/?ref=page_internal')

        sleep(random.uniform(4.0, 5.0))
        self.driver.find_element("xpath", '//div[@class="om3e55n1 obv5v25f rl78xhln aesu6q9g srn514ro"]').click()

        sleep(random.uniform(1.0, 2.0))
        self.driver.find_element("xpath", '//div[@class="alzwoclg cqf1kptm cgu29s5g om3e55n1"]').click()

        dataset = {'nombre': [], 'review': [], 'date_extract' : []}
        
        sleep(random.uniform(1.0, 2.0))
        get_container_reviews = self.driver.find_elements("xpath", '//div[@class="g4tp4svg mfclru0v om3e55n1 p8bdhjjv"]')

        for container in get_container_reviews:
            nombre     = container.find_element("xpath", './/span[@class="gvxzyvdx aeinzg81 t7p7dqev gh25dzvf exr7barw k1z55t6l oog5qr5w tes86rjd rtxb060y"]/strong[1]//span[@class="rse6dlih"]').text
            try:
                review = container.find_element("xpath", './/div[@class="m8h3af8h l7ghb35v kjdc1dyq kmwttqpk gh25dzvf n3t5jt4f"]/div').text
            except NoSuchElementException:
                review = container.find_element("xpath", './/div[@class="m8h3af8h l7ghb35v kjdc1dyq kmwttqpk gh25dzvf"]').text
            
            
            # Delete Emoji
            review = aux_text.delete_emoji(review)

            dataset['nombre'].append(nombre)
            dataset['review'].append(review)
            dataset['date_extract'].append(self.date)

        return self.dowload_csv(dataset)
