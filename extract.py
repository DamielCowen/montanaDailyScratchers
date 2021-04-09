import json
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime

path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
url = 'https://www.montanalottery.com/en/view/scratch'

# disables chrome from loading images 
# https://stackoverflow.com/questions/28070315/python-disable-images-in-selenium-google-chromedriver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

#creates a selenium chrome driver
driver = webdriver.Chrome(path_to_chromeDriver,options=chrome_options)
driver.implicitly_wait(5)
driver.get(url)
soup = BeautifulSoup(driver.page_source)
driver.close()

scratchGameLobby = soup.find("div",{"class":"scratch-game-lobby row remove-gutter bgg-main"}) #finds the center column with all game data
scratchGameResultSet = scratchGameLobby.findAll("div",{"class":"row scratch-game pad50 mg0"}) #splits games into a BS resultset

def getGameName(gameTag):
    '''
    scratchGameResultSet:gameTag(bs4.element.tag) -> name of the game (str)
    '''
    return gameTag.find("span",{"class":"scratch-game-title cr-main text-uppercase pull-left"}).text

def getGameOverallOdds(gameTag):
    '''
    scratchGameResultSet:gameTag(bs4.element.tag) -> overall Odds (str)
    '''
    return gameTag.find("td", {"class":"text-center text-uppercase overall-odds"}).text

def getGamePrice(gameTag):
    '''
    scratchGameResultSet:gameTag(bs4.element.tag) -> game ticket cost (str)
    '''
    parent = gameTag.find_parent()
    return parent.h2.text

def getGameRowData(gameTag):
    '''
    scratchGameResultSet:gameTag(bs4.element.tag) -> list of rows where each row is a dictonary containing 
    {win:str,priz:str:odds:str}
    '''
    tbody =gameTag.tbody
    output = []
    rows = tbody.findAll('tr')
    for row in rows[:-1]:
        output.append({list(row.children)[1]['data-bind'].strip('text: '):list(row.children)[1].text, #win
         list(row.children)[3]['data-bind'].strip('text: '):list(row.children)[3].text, #priz
         list(row.children)[5]['data-bind'].strip('text: '):list(row.children)[5].text,  #odds   
        })
    return output

today = datetime.today().strftime('%Y%m%d')
games_data = {"date":today}
game_data = []

for gameTag in scratchGameResultSet:
    output = {}
    output['name'] = getGameName(gameTag)
    output['overallOdds'] = getGameOverallOdds(gameTag)
    output["price"] = getGamePrice(gameTag)
    output['data'] = getGameRowData(gameTag)
    game_data.append(output)
games_data['data'] = game_data


with open(f'data/{today}_scratchers.json', 'w') as fp:
    json.dump(games_data, fp)