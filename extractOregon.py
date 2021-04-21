import src.scratch

class ORscratch(src.scratch.ExtractScratch):

    def __init__(self):
        super().__init__()
        self.URL = 'https://www.oregonlottery.org/scratch-its/grid/'
    
    
    def get_Oregon_scatch_game_links(self):
        '''
        sends driver to OR scratch grid and gets the java var scratchIts which contains the urls to each game. 
        
        '''
        self.driver.get(self.URL)
        self.game_details_dict = self.driver.execute_script("return scratchIts")
      

    def get_game_data(self,game_url):
        self.driver.get(game_url)
        try:
            output = self.driver.execute_script("return scratchGame")
        except JavasciptException:
            output = None
            
        return output
    
    def get_games_data(self):
        self.get_Oregon_scatch_game_links()     
        self.games_data = [self.get_game_data(game['link']) for game in self.game_details_dict]
                                        
    
    def extract_Oregon(self):
        
        self.chrome_driver()
        self.get_games_data()
        self.save_json("Oregon", "OR")
        self.driver.close()
        
if __name__ == "__main__":
    OR = ORscratch()
    OR.extract_Oregon()
