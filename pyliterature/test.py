from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

url = 'http://www.sciencedirect.com/science/article/pii/S1751616116301138'
# url = 'http://pubs.acs.org/doi/full/10.1021/jz5009483'
keyword = 'CALPHAD'


driver = webdriver.Firefox(options = options)
driver.get("http://www.python.org")
print(driver.page_source)
driver.close()
