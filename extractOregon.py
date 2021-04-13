import json
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime




def getOregonScatchGameLinks(driver):
    driver.get(url)
    gameDetailsDict = driver.execute_script("return scratchIts")
    return gameDetailsDict

    
def getGameData(driver, url):
    driver.get(url)
    return driver.execute_script("return scratchGame")


# disables chrome from loading images 
# https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

#creates a selenium chrome driver
path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
driver = webdriver.Chrome(path_to_chromeDriver,options=chrome_options)
driver.implicitly_wait(5)

url = "https://www.oregonlottery.org/scratch-its/grid/"
driver.get(url)

#contains links to individual games
gameMetaData = getOregonScatchGameLinks(driver)

gamesData = [getGameData(driver, game["link"]) for game in gameMetaData]


today = datetime.today().strftime('%Y%m%d')
with open(f'data/oregon/{today}_ORscratchers.json', 'w') as fp:
    json.dump(gamesData, fp)
