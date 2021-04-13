import json
from selenium import webdriver
from datetime import datetime

path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
url ='https://www.walottery.com/Scratch/'

# disables chrome from loading images 
# https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

#creates a selenium chrome driver
driver = webdriver.Chrome(path_to_chromeDriver,options=chrome_options)
driver.implicitly_wait(5)
driver.get(url)
games_data = driver.execute_script('return WaLottery.Scratch.data')
driver.close()

today = datetime.today().strftime('%Y%m%d')
with open (f"data/washington/{today}_WAscratchers.json", "w") as file:
    json.dump(games_data, file)
    
    