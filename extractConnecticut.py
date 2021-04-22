import src.scratch
import requests
from bs4 import BeautifulSoup

class CTscratch(src.scratch.ExtractScratch):
    '''
    imports src.scratch, requests, BS4
    
    -get_scratch_game_URLs(): goes to list page and gets links for all games
        --self.game_URLs
    -get_game_data(): gets data from game page: top and lower table
        --get_top_table(): returns dict of game details
        --get_lower_table(): returns table of unclaimed prizes
    
    '''
    def __init__(self):
        super().__init__()
        self.URL = 'https://www.ctlottery.org/ScratchGamesTable'
        self.URL_PREFIX = 'https://www.ctlottery.org/'
        
    def get_soup(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content,features="lxml")
        return soup       
    
    def get_scratch_game_URLs(self):
        soup = self.get_soup(self.URL)
        table = soup.table.tbody
        rows = table.findAll('a')
        self.game_URLs = [self.URL_PREFIX+row['href'] for row in rows]
        
    def get_game_data(self,URL):
        soup = self.get_soup(URL)
        game_data = self.get_top_table(soup)
        game_data['URL'] = URL
        game_data['unclaimed'] = self.get_lower_table(soup)
        return game_data
    
    def get_game_name(self,soup):
        return soup.h2.text
    
    def get_date(self, text):
        return text.split(':')[-1]
    
    def get_lower_table_date(self, table):
        text = table.h3.text
        return text.split(' ')[-1] 
        
    def get_top_table(self, soup):
        rows = soup.table.tbody.findAll("tr")
        self.rows = rows
        game_data = {}
        game_data['Name'] = self.get_game_name(soup)
        game_data['Start'] = self.get_date(rows[0].text)
        game_data['Cost'] = self.string_to_float(rows[1].text)
        game_data['TopPrize'] = self.string_to_float(rows[2].text)
        game_data['End'] = self.get_date(rows[3].text)
        game_data['Last'] = self.get_date(rows[4].text)
        game_data['TotalTickets'] = self.string_to_float(rows[5].text)
        game_data['Odds'] = rows[6].text
        game_data['Status'] = rows[7].text
        return game_data
    
    def get_lower_table(self,soup):
        table = soup.find("div",{"class":"unclaimed-prize-wrap text-center"})
        rows = table.tbody.find_all('tr')
        output = {}
        output['date'] = self.get_lower_table_date(table)
        table_data = []
        for row in rows:
            cell_data = row.find_all('td')
            row_data = {}
            row_data['Amount'] = cell_data[0].text
            row_data['TotalPrizes'] = cell_data[1].text
            row_data['Unclaimed'] = cell_data[2].text
            table_data.append(row_data)
        output['data'] = table_data
        return output
    
    def get_games_data(self):
        self.games_data = [self.get_game_data(URL) for URL in self.game_URLs]
        
    def extract_Connecticut(self):
        self.get_scratch_game_URLs()
        self.get_games_data()
        self.save_json('connecticut',"CT")
        
        
        
if __name__ =="__main__":
    CT = CTscratch()
    CT.extract_Connecticut()
        
