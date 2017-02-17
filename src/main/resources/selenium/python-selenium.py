from selenium import webdriver

# Create a new instance of the firefox driver
desired_cap = {
    'browserName': "firefox",
}
driver = webdriver.Remote(
   command_executor='http://localhost:4444/wd/hub',
   desired_capabilities=desired_cap)

try:
   # go to the google home page
   driver.get("http://www.google.com")
   output = driver.title
finally:
    driver.quit()
