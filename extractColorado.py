import src.scratch
from bs4 import BeautifulSoup


class COscratch(src.scratch.ExtractScratch):

    def __init__(self):
        '''
        Extract Colorado:
        -Imports: BS4, src.scract
        -get_games_data() selenium goes to grid page and gets URLs for all games.
        -- saves links to game_URLs
        -get_all_games_data() sends selenium to each page and scrapes game data
        -- saves to games_data list(dicts{})
        - saves json
        
        '''
        super().__init__()
        self.URL = 'https://www.coloradolottery.com/en/games/scratch/'
        
    def get_games_data(self):
        '''
        creates chrome driver instance, goes to scratch grid URL and gets a list of links to all scratch games. savers to self.game_URLs
        '''
        self.chrome_driver()
        self.driver.get(self.URL)
        soup = BeautifulSoup(self.driver.page_source,features="lxml")
        games_data = soup.select('#game-list')[0]
        self.game_URLs = [game['href'] for game in games_data.find_all("a",{"class":"flyoutTrigger"})]
        self.games_data = []
        
        
    def get_game_data(self, game_URL):
        '''
        after get_games_data is called -> takes an individual game URL and returns details in ditconary
        '''
        self.driver.get(game_URL)
        soup = BeautifulSoup(self.driver.page_source, features ="lxml")
        output = {"name":self.get_game_name(soup),
                  "cost":self.get_game_cost(soup),
                  "top_prize":self.get_top_prize(soup),
                  "top_prizes_remaining":self.get_top_prize_remaining(soup),
                  "last_day_claim":self.get_last_day_to_claim(soup),
                  "payout_precentage":self.get_payout_percentage(soup),
                  "data": self.get_row_data(soup)
                 }
        return output
        

    
    def get_game_name(self,soup):
        return soup.h1.text

    def get_game_cost(self,soup):
        asString = soup.select('#tabGameDetails > p:nth-child(3)')[0].text
        asFloat = self.string_to_float(asString)
        return asFloat

    def get_top_prize(self,soup):
        asString = soup.select('#tabGameDetails > p:nth-child(4)')[0].text
        asFloat = self.string_to_float(asString)
        return asFloat

    def get_top_prize_remaining(self,soup):
        asString = soup.select('#tabGameDetails > p:nth-child(5)')[0].text
        asFloat = self.string_to_float(asString)
        return asFloat

    def get_last_day_to_claim(self,soup):
        return soup.select('#tabGameDetails > p:nth-child(6)')[0].text

    def get_payout_percentage(self, soup):
        asString = soup.select('#tabGameDetails > p:nth-child(7)')[0].text
        asFloat = self.string_to_float(asString)
        return asFloat
    
    def get_row_data(self, soup):
        table = soup.table.tbody
        output = []
        for row in table.find_all("tr"):
            amount = self.string_to_float(row.find_all("td")[0].text)
            number = self.string_to_float(row.find_all("td")[1].text)
            odds = row.find_all("td")[2].text
            row_data = {
                "amount":amount,
                "number":number,
                "odds" :odds}
            output.append(row_data)
        return output
    
    def get_all_games_data(self):
        self.games_data = [self.get_game_data(url) for url in self.game_URLs]
        
 
    def extract_Colorado(self):
        self.get_games_data()
        self.get_all_games_data()
        self.save_json("colorado","CO")
        self.driver.close()

    
        
if __name__ == "__main__":
    CO = COscratch()
    CO.extract_Colorado()

