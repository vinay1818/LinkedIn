from selenium import webdriver
import time
from bs4 import BeautifulSoup
import xlsxwriter
from tkinter import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd 
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
class Linkedin():
    def getData(self):
      


        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get('https://www.linkedin.com/login')
        username_input = driver.find_element("id", "username")
        username_input.send_keys(os.environ.get('email'))
        
        driver.find_element("id", "password").send_keys(os.environ.get('password'))  #Enter Password of linkedin account here
        driver.find_element("xpath","//*[@type='submit']").click()


        #*********** Search Result ***************#
        page_num = 2
        search_key = "data analyst" # Enter your Search key here to find people
        key = search_key.split()
        keyword = ""
        for key1 in key:
            keyword = keyword + str(key1).capitalize() +"%20"
        keyword = keyword.rstrip("%20")
            
        global data
        data = []

        for no in range(1,page_num):
            start = "&page={}".format(no) 
            search_url = "https://www.linkedin.com/search/results/people/?keywords={}&origin=SUGGESTION{}".format(keyword,start)
            driver.get(search_url)
            driver.maximize_window()
            for scroll in range(2):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
            search = BeautifulSoup(driver.page_source,'lxml')
            
        
            print("Going to scrape Page {} data".format(no))
            
            # Find the meta tag with the specified attribute
            profiles = search.findAll('li', attrs = {'class':'reusable-search__result-container'})

            for profile in profiles:
                
                a_tag = profile.find('a', class_='app-aware-link')

                # Extract the value of the href attribute
                if a_tag:
                    href_value = a_tag.get('href')
                    
                img_tag = profile.find('img')

                # Extract the value of the alt and src attributes
                if img_tag:
                    title = img_tag.get('alt')
                    profile_pic = img_tag.get('src')
                  
                
                    
                # Find the <div> tags with the specified class names
                primary_subtitle = profile.find('div', class_='entity-result__primary-subtitle')
                secondary_subtitle = profile.find('div', class_='entity-result__secondary-subtitle')

               
                role = primary_subtitle.get_text(strip=True)
                loc = secondary_subtitle.get_text(strip=True)
                    
                    
                data.append({'Name':title,'profile_url':href_value,'profile_pic':profile_pic,'loc':loc,'role':role,})
            print("!!!!!! Data scrapped !!!!!!")
        
        df = pd.DataFrame(data)
       
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")

        file_name = f'Profiles-{timestamp}'
        df.to_excel(f"{file_name}.xlsx")      
        driver.quit()
    

    def start(self):
        self.getData()
        
if __name__ == "__main__":
    obJH = Linkedin()
    obJH.start()
