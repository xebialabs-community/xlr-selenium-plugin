import sys, json, __builtin__
from selenium.SeleniumRunner import SeleniumRunner

testcase = '''
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
import json

desired_capabilities = %s
command_executor = '%s'

driver = webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities)

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

# go to the google home page
driver.get("http://www.google.com")

# the page is ajaxy so the title is originally this:
print driver.title + "\\n"

# find the element that's name attribute is q (the google search box)
inputElement = driver.find_element_by_name("q")

# type in the search
inputElement.send_keys("cheese!")

# submit the form (although google automatically searches now without submitting)
inputElement.submit()

# we have to wait for the page to refresh, the last thing that seems to be updated is the title
WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

# You should see "cheese! - Google Search"
print driver.title + "\\n"

driver.close()
''' % (json.dumps(configuration.desiredCapabilities), configuration.commandExecutor)

if configuration.host:
    script = SeleniumRunner(testcase, "ssh", configuration.host, configuration.password)
else:
    script = SeleniumRunner(testcase)

exitCode = script.execute()
output = script.getStdout()

if (exitCode == 0):
    logger.info(output)
else:
    logger.info(testcase)
    logger.info("---")
    logger.info("Exit code ")
    logger.info(str(exitCode))
    logger.info("")
    logger.info("#### Output:")
    logger.info(output)

    logger.info("#### Error stream:")
    logger.info(script.getStderr())
    logger.info("")
    logger.info("----")

    sys.exit(exitCode)

