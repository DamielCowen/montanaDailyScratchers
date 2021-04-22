import src.scratch
import requests
from bs4 import BeautifulSoup

class ARscratch(src.scratch.ExtractScratch):
    '''
    imports src.scratch, requests, BS4
    
    -get_links_from_all_pages(): Sends requests to scratch game grid page, 
                        gets all URLs from that grid page and goes to next page
        -get_page_URLs(): gets all URLs from a grid page
    -get_game_data(): gets all game data from the game page
    '''
    
    
    def get_links_from_all_pages(self):
        '''
        goes to the next page, and recovers all links. When the number of links == 0 returns the collected links.
            
        '''
        BASE_URL = 'https://www.myarkansaslottery.com/games/instant?amount=All&page='
        self.game_URLs= []
        page_number = 0
        while True:
            next_URL = BASE_URL+str(page_number)
            response = requests.get(next_URL)
            soup = BeautifulSoup(response.content, features="lxml")
            URLs = self.get_page_URLs(soup)
            if len(URLs) == 0:
                break
            self.game_URLs.extend(URLs)
            page_number += 1
        
    def get_page_URLs(self, soup):
        '''
        input: soup for a games grid page
        output: list of all game URLs on that page
        '''
        URL_PREFIX = 'https://www.myarkansaslottery.com'
        page_content = soup.find("div",{"class":"view-content"})
        if page_content is None:
            return []
        games_headers = page_content.findAll("h2")
        URLs= [URL_PREFIX+game.find("a")["href"] for game in games_headers]
        return URLs
    
    
    def get_game_name(self, soup):
        return soup.h1.text

    def get_game_cost(self, soup):
        div = soup.find("div",{"class":"field field-name-field-ticket-price field-type-text field-label-above layout-3col__col-x"})
        asString = div.find("div",{"class":"field-item even"}).text
        asFloat = self.string_to_float(asString)
        return asFloat

    def get_prize_odds(self, soup):
        div = soup.find("div",{"class":"field field-name-field-game-odds field-type-text field-label-above layout-3col__col-x"})
        asString = div.find("div",{"class":"field-item even"}).text.split(' ')[-1]
        asFloat = self.string_to_float(asString)
        return asFloat

    def get_total_amount_remaining(self, soup):
        css_selector = 'div.layout-center:nth-child(7) > div:nth-child(1)'
        div = soup.select(css_selector)
        _,_,_,asString = list(soup.select('div.layout-center:nth-child(7) > div:nth-child(1)'))[0].text.split(" ")
        asFloat = self.string_to_float(asString)
        return asFloat

    def get_game_table_data(self, soup):
        rows = soup.html.body.table.tbody.findAll("tr")
        table = []
        for row in rows:
            row_data = {}
            row_data['Tier'] = row.find("td",{"data-cell-title":"Tier Prize Description:"}).text
            row_data['TotalPrizes'] = self.string_to_float(row.find("td",{"data-cell-title":"Total Prizes:"}).text)
            row_data['RemainingPrizes']= self.string_to_float(row.find("td",{"data-cell-title":"Total Prizes:"}).text)
            row_data['TotalValue'] = self.string_to_float(row.find("td",{"data-cell-title":"Total Prize Amount:"}).text)
            row_data['RemainingValue'] = self.string_to_float(row.find("td",{"data-cell-title":"Estimated Prize Amount Remaining:"}).text)
            table.append(row_data)
        return table

    def scrape_game_page(self, soup):
        game_data = {}
        game_data['Name'] = self.get_game_name(soup)
        game_data['Cost'] = self.get_game_cost(soup)
        game_data['Odds'] = self.get_prize_odds(soup)
        game_data['Remaining_Amount'] = self.get_total_amount_remaining(soup)
        game_data['Data'] = self.get_game_table_data(soup)
        return game_data

    def extract_Arkansas(self):
        self.get_links_from_all_pages()
        self.games_data = []
        for url in self.game_URLs:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, features="lxml")
            self.games_data.append(self.scrape_game_page(soup))
        self.save_json("arkansas",'AR')
        
        
        
if __name__ =='__main__':
    AR = ARscratch()
    AR.extract_Arkansas()
        
    

    
