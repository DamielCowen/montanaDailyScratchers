from selenium import webdriver

class Requests:
    
    def __init__(self,url):
        self.url = url
    

    def getSeleniumRequest(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_opitons.add_argument("--no-sandbox")
            
            #creates a selenium chrome driver
            path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
            driver = webdriver.Chrome(path_to_chromeDriver,options=chrome_options)
            driver.implicitly_wait(5)
            return driver
        except:
            pass
