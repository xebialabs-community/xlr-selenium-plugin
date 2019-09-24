#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys, json, __builtin__
from selenium.SeleniumRunner import SeleniumRunner
from selenium.RemoteScriptRetriever import RemoteScriptRetriever
import json
import logging
import os

logger = logging.getLogger(__name__)
allScriptsDict = {}
finalOutputList = ['## Results Report',' ','Test Name | Pass/Fail', ':---: | :---:']
finalDetailsList = []
finalExitCode = 0


# Determine if running a single script or retrieving multiple scripts
# then store test script in allScriptsDict
method = str(task.getTaskType())
if method == "selenium.RunScriptsRetrievedFromRepository":
    scriptRetriever = RemoteScriptRetriever(targetURL, repositoryUsername, repositoryPassword, failIfFileNotFound)
    logger.debug("targertURL = %s, repositoryUsername=%s,  repositoryPassword=%s, failIfFileNotFound=%s" %
        (targetURL, repositoryUsername, repositoryPassword, str(failIfFileNotFound)))
    for key in fileMap:
        allScriptsDict.update({key:scriptRetriever.getData(fileMap[key])})
elif method == "selenium.RunSinglePythonTestCase":
    allScriptsDict.update({testCaseName:testCase})

# Determine if we will execute scripts remotely and which password to use
password = ''
runRemote = False
if host:
    runRemote = True
    if hostPassword:
        password = hostPassword
    else:
        password = host.get("password")

# Run tests stored in allScriptsDict
for key in allScriptsDict:
    currentTestName = key
    currentTestCase = allScriptsDict[key]
    if runRemote:
        testCaseRunner = SeleniumRunner(currentTestCase, "ssh", host, password)
    else:
        testCaseRunner = SeleniumRunner(currentTestCase)
    exitCode = testCaseRunner.execute()
    if exitCode != 0:
        finalExitCode = 1
    output = testCaseRunner.getStdout()
    additionalStream = testCaseRunner.getStderr()
    finalOutputList.append("%s|%s" % 
        (currentTestName, 
        'Passed' if exitCode == 0 else 'Failed'))
    detailObject = {}
    detailObject.update({'testName': key})
    detailObject.update({'result': ('Passed' if exitCode == 0 else 'Failed')})
    detailObject.update({'output': output})
    if detailObject["result"] == "Passed":
        addStr = additionalStream.replace('-','').replace('.','',1).replace('\n\n', '  \n').replace('\n','',1)
    else:
        addStr = additionalStream
    detailObject.update({'additionalStream': addStr})
    finalDetailsList.append(detailObject)
    
# report and exit
# set output variable outputJson
#outputJson = json.dumps(finalDetailsList, sort_keys=False,
#                 indent=4, separators=(',', ': '))
outputJson = finalDetailsList

# print table
for item in finalOutputList:
    print(item)
# print details
print(' ')
for item in finalDetailsList:
    print(' ---  ')
    print(' ### %s : %s  ' % (item['testName'], item["result"]))
    print(' %s :  ' % ('Script Output'))
    print('>%s   ' % ( item["output"]))
    print('  ')
    print('  %s :  ' % ('Additional Information'))
    print('>%s   ' % ( item["additionalStream"]))
    print('  ')
    
if finalExitCode != 0:
    sys.exit(exitCode)











