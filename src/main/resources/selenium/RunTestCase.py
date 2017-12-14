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

driver = webdriver.Remote(
            command_executor=command_executor,
            desired_capabilities=desired_capabilities)

# payload goes here
%s
# end payload

driver.close()
''' % (json.dumps(capabilitiesDict), seleniumProfile['commandExecutor'], testCase)


host = seleniumProfile['host']
password = seleniumProfile['password']
if host:
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

