#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
from selenium.SeleniumRunner import SeleniumRunner
from selenium.RemoteScriptRetriever import RemoteScriptRetriever
import json
import logging
import os

logger = logging.getLogger(__name__)

class RunTestCases():
    def __init__(self, allScriptsDict, runRemote, host=None, password = None, failOnFirstFailure=True):
        self.logger = logger
        self.allScriptsDict = allScriptsDict
        self.runRemote = runRemote
        self.host = host
        self.password = password
        self.failOnFirstFailure = failOnFirstFailure
        self.logger.debug("In RunTestCases init")


    def runTests(self):
        finalOutputList = ['## Results Report',' ','Test Name | Pass/Fail', ':---: | :---:']
        finalDetailsList = []
        finalExitCode = 0

        # Run tests stored in allScriptsDict
        for key in self.allScriptsDict:
            currentTestName = key
            currentTestCase = self.allScriptsDict[key]
            if self.runRemote:
                selRunner = SeleniumRunner(currentTestCase, "ssh", self.host, self.password)
            else:
                selRunner = SeleniumRunner(currentTestCase)
            exitCode = selRunner.execute()
            
            # assume passing
            outcome = 'Passed'
            if exitCode !=0:
                # If test failed, we will set finalExitCode to error exitCode. Depending upon configuration,
                # we may continue testing but finalExitCode will never be set back to 0
                # because we ultimately want the whole task to fail upon completion of tests.
                finalExitCode = exitCode
                outcome = 'Failed'
            elif len(currentTestCase) == 0:
                outcome = 'Not Found'
            output = selRunner.getStdout()
            additionalStream = selRunner.getStderr()
            finalOutputList.append("%s|%s" % 
                (currentTestName, outcome))
            detailObject = {}
            detailObject.update({'testName': key})
            
            detailObject.update({'result': outcome})
            detailObject.update({'output': output})
            if detailObject['result'] == 'Passed':
                addStr = additionalStream.replace('-','').replace('.','',1).replace('\n\n', '  \n').replace('\n','',1)
            else:
                addStr = additionalStream.replace('===','').replace('-','').replace('\n\n', '  \n').replace(' \n \n','\n').replace(' \n  \n','\n')
            detailObject.update({'additionalStream': addStr})
            logger.debug('About to append detailObject - %s' % detailObject)
            finalDetailsList.append(detailObject)
            if self.failOnFirstFailure and finalExitCode != 0:
                break
        
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

        return json.dumps(finalDetailsList), finalExitCode
        
        











