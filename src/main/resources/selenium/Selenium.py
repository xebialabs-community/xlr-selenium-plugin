#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from selenium import webdriver
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
#from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

class SeleniumClient(object):
    def __init__(self):
        return

    @staticmethod
    def get_client():
        return SeleniumClient()

    def testing_seleniumexample(self, variables):
        print "Starting Selenium Test Example..."
        output = ""
        desired_cap = {
            'browserName': "firefox",
        }
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            desired_capabilities=desired_cap)
        print "driver: %s" % driver
        # go to the google home page
        driver.get("http://www.google.com")
        # the page is ajaxy so the title is originally this:
        output += "%s\n" % driver.title
        # find the element that's name attribute is q (the google search box)
        inputElement = driver.find_element_by_name("q")
        # type in the search
        inputElement.send_keys("cheese!")
        # submit the form (although google automatically searches now without submitting)
        inputElement.submit()
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

            # You should see "cheese! - Google Search"
            output += "%s\n" % driver.title
        finally:
            driver.quit()
        return {"output" : "SUCCESS"}
