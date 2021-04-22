import json
from selenium import webdriver
from datetime import datetime
from re import sub

class ExtractScratch():
    
    def __init__(self):
        self.path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
        
    def chrome_driver(self):
        """
        creates a selenium chrome web driver instance with select options 
        -disables chrome from loading images 
            -https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
        """
        self.chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(self.path_to_chromeDriver,options=self.chrome_options)
        self.driver.implicitly_wait(5)
        
        
    def random_user_agent(self):
        pass
        
    def string_to_float(self, s):
         return float(sub(r'[^\d.]', '', s))

        
    def save_json(self, state,abbreviation):

        today = datetime.today().strftime('%Y%m%d')
        with open (f"data/{state}/{today}_{abbreviation}scratchers.json", "w") as file:
            json.dump(self.games_data, file)
            
                    
