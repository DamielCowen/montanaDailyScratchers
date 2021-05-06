import requests
import src.scratch
from bs4 import BeautifulSoup

class ILscratch(src.scratch.ExtractScratch):
    
    def __init__(self):
        super().__init__()
        self.URL = 'https://www.illinoislottery.com/games-hub/instant-tickets'
        
    def get_URLs_from_page(self, soup):
        '''
        returns list of all game URLs on a page
        '''
        BASE_URL = 'https://www.illinoislottery.com'
        game_cards = soup.find_all("div",{"class":"simple-game-card__content prize"})
        return [BASE_URL+game.find('a')['href'] for game in game_cards]
        
    def get_game_URLs(self):
        '''
        input: soup for a games grid page
        output: list of all game URLs on that page
        
        iterates through pages until no games data is returned
        '''
        BASE_URL = 'https://www.illinoislottery.com/games-hub/instant-tickets?page='
        self.game_URLs = []
        page_number = 0
        while True:
            next_URL = BASE_URL+str(page_number)
            soup = self.request_soup(next_URL)
            URLs = self.get_URLs_from_page(soup)
            if len(URLs) == 0:
                break
            self.game_URLs.extend(URLs)
            page_number += 1
        
        
    def get_game_data(self,URL):
        soup = self.request_soup(URL)
        table = self.get_top_table_data(soup)
        game_data = self.extract_from_top_table(table)
        game_data['name'] = self.get_game_name(soup)
        return game_data
    
    def get_top_table_data(self, soup):
        table = soup.table.tbody
        rows = table.find_all('tr')
        table_data = {}
        for row in rows:
            row_info = row.find_all('td')
            table_data[row_info[0].text] = row_info[1].text
        return table_data
    
    def extract_from_top_table(self, table):
        output = {}
        try:
            output['cost'] = self.string_to_float(table['Price Point'])
        except KeyError:
            pass
        try:
            output['launch_date'] = table['Launch Date']
        except KeyError:
            pass
        try:
            output['game_number'] = table['Game Number']
        except KeyError:
            pass
        try:
            output['odds'] = table['Overall Odds']
        except KeyError:
            pass 
        return output        

    def get_game_name(self, soup):
        #print(soup.title.text.split(' | ')[0])
        return soup.title.text.split(' | ')[0]

    def get_games_data(self):
        self.games_data = [self.get_game_data(URL) for URL in self.game_URLs]
        
    def extract_Illinois(self):
        self.get_game_URLs()
        self.get_games_data()
        self.save_json('illinois',"IL")
        
        
if __name__ =="__main__":
    IL = ILscratch()
    IL.extract_Illinois()
