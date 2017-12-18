#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, json, __builtin__
from selenium.SeleniumRunner import SeleniumRunner

# XLR gives us back a view that isn't a Python dict - convert it first
# so we can dump it to json later
capabilitiesDict = {}
for key in seleniumProfile['desiredCapabilities']:
    capabilitiesDict[key] = seleniumProfile['desiredCapabilities'][key]

testcaseWrapperWithPayload = '''
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

desired_capabilities = %s
command_executor = '%s'

driver = webdriver.Remote(command_executor=command_executor,desired_capabilities=desired_capabilities)

# payload goes here
%s
# end payload

driver.close()
''' % (json.dumps(capabilitiesDict), seleniumProfile['commandExecutor'], testCase)

host = seleniumProfile['host']
if host:
    password = seleniumProfile['password']
    testCaseRunner = SeleniumRunner(testcaseWrapperWithPayload, "ssh", host, password)
else:
    testCaseRunner = SeleniumRunner(testcaseWrapperWithPayload)

exitCode = testCaseRunner.execute()
output = testCaseRunner.getStdout()

if (exitCode == 0):
    print output
    print("---")
    print "SeleniumRunner exited successfully"
else:
    print("---")
    print("Exit code ")
    print(str(exitCode))
    print("")
    print("#### Output:")
    print(output)

    print("#### Error stream:")
    print(testCaseRunner.getStderr())
    print("")
    print("----")

    sys.exit(exitCode)

