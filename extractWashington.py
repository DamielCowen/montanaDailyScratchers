import json
from selenium import webdriver
from datetime import datetime


class scrapeScratchGames:
    
    def __init__(self):
        self.URL ='https://www.walottery.com/Scratch/'
        self.path_to_chrome_driver = '/Users/drahcir1/Documents/montanaDailyScratchers/src/chromedriver'
        
    def chrome_driver(self):
        """
        creates a selenium chrome web driver instance with select options 
        -disables chrome from loading images 
            -https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
        """
        self.chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(self.path_to_chrome_driver,options=self.chrome_options)
        self.driver.implicitly_wait(5)
        
    def get_games_data(self):
        '''
        Washington lotto has a convinent json dictonary that can be accessed with the single line below.
        Thank you Bye and Bye State
        
        retrives the varialbe and closes the driver
        
        ''' 
        self.driver.get(self.URL)
        self.games_data = self.driver.execute_script('return WaLottery.Scratch.data')
        self.driver.close()
        
    def save_json(self):

        today = datetime.today().strftime('%Y%m%d')
        with open (f"data/washington/{today}_WAscratchers.json", "w") as file:
            json.dump(self.games_data, file)
            
            
    def extract_Washington(self):
        self.chrome_driver()
        self.get_games_data()
        self.save_json()
        
        
if __name__ =="__main__":
    WA = scrapeScratchGames()
    WA.extract_Washington()
