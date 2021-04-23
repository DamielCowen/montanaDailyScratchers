import requests
import src.scratch
from bs4 import BeautifulSoup

class FLscratch(src.scratch.ExtractScratch):
    
    def __init__(self):
        super().__init__()
        self.URL = 'http://www.flalottery.com/scratch-offs'
    
    def get_ticketDetails_tag(self):
        soup = self.request_soup(self.URL)
        self.games_details =  soup.find_all("div", {"class":"ticketDetails"})
    
    def get_game_data(self, tag):
        game_data = {}
        game_data['name'] = self.get_game_name(tag)
        game_data.update(self.get_game_cost_and_dates(tag))
        game_data['data'] = self.get_table_data(tag)
        return game_data
    
    def get_table_data(self,tag):
        table_data = []
        rows = tag.tbody.find_all('tr')
        for row in rows:
            row_data = {}
            cells = row.find_all('td')
            row_data['Amount'] = self.string_to_float(cells[0].text)
            row_data['Odds'] = cells[1].text
            row_data['Total'] = self.string_to_float(cells[2].text)
            row_data['Remaining'] = self.string_to_float(cells[3].text)
            table_data.append(row_data)
        return table_data

    def get_game_name(self, tag):
        return tag.span.text
    
    def get_game_details_paragraph(self, tag):
        '''
        Iterates through the "How to Play" paragraphs and returns the one wtih
        the game details.
        
        '''
        for p in tag.find_all('p'):
            if "Ticket Price" in p.text:
                return p
    
    def get_game_cost_and_dates(self, tag):
        '''
        Game cost and dates are one of the "How to Play" paragraphs
        This function returns them as a dictonary.
         
        '''
        details_paragraph = self.get_game_details_paragraph(tag)
        details = details_paragraph.find_all('strong')
        output = {}
        output['Cost'] = self.string_to_float(details[0].next_sibling)
        output['Start'] = details[1].next_sibling
        output['End'] = details[2].next_sibling
        output['RedeemBy'] = details[3].next_sibling
        return output
    
    def get_games_data(self):
        self.games_data = [self.get_game_data(tag) for tag in self.games_details]
        
    def extract_Florida(self):
        self.get_ticketDetails_tag()
        self.get_games_data()
        self.save_json('florida','FL')
        

        
if __name__ == "__main__":
    
    FL = FLscratch()
    FL.extract_Florida()
        
        
    