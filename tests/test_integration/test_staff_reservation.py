from selenium import webdriver

options = webdriver.FirefoxOptions()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.get("http://localhost:8000")

assert "BnB" in browser.title


browser.quit()
