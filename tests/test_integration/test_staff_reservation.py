from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.get("http://localhost:8000")

assert "BnB" in browser.title


browser.quit()
