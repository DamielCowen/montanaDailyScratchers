from selenium import webdriver
from datetime import datetime

path_to_chromeDriver = '/Users/drahcir1/Documents/chromedriver'
url = 'https://www.montanalottery.com/en/view/scratch'

def saveHTML(page_contents):
    today = datetime.today().strftime('%Y%m%d')
    with open (f"data/{today}_scratchers.html", "w") as file:
        file.write(page_contents)

driver = webdriver.Chrome(path_to_chromeDriver)
driver.implicitly_wait(5)
driver.get(url)
saveHTML(driver.page_source)

        