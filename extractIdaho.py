import json
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
from re import sub


def stringToFloat(s):
     return float(sub(r'[^\d.]', '', s))
def getGameName(gameTag):
    return gameTag.h5.text

def getGameCost(gameTag):
    string = gameTag.find("span", {"game__info-price"}).text
    return stringToFloat(string)

def getGameRowPrize(rowTag):
    priceString = rowTag.find("td",{"class":"prizes-prize"}).text
    return stringToFloat(priceString)

def getGameRowPrizesRemaining(rowTag):
    remainingString = rowTag.find("td",{"class":"prizes-remaining"}).text
    return stringToFloat(remainingString)  

def getGameRowData(gameTag):
    output = []
    tbody = gameTag.tbody
    for row in tbody.findAll('tr'):
        output.append({"PrizeAmount":getGameRowPrize(row),
                       "PrizesRemaining":getGameRowPrizesRemaining(row)})
    return output


path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
url ='https://www.idaholottery.com/games/scratch'

# disables chrome from loading images 
# https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

#creates a selenium chrome driver
driver = webdriver.Chrome(path_to_chromeDriver,chrome_options=chrome_options)
driver.implicitly_wait(5)
driver.get(url)
soup = BeautifulSoup(driver.page_source)
driver.close()

games = soup.findAll("div",{"class":"game__content"})
today = datetime.today().strftime('%Y%m%d')
games_data = {"date":today}
gamesContent = []
for gameTag in games:
    game_data = {}
    game_data["name"] = getGameName(gameTag)
    game_data["cost"] = getGameCost(gameTag)
    game_data["data"] = getGameRowData(gameTag)
    gamesContent.append(game_data)
    
    
games_data['data'] = gamesContent

with open (f"data/idaho/{today}_IDscratchers.json", "w") as file:
    json.dump(games_data, file)
    