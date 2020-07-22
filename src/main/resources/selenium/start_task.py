#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import selenium
import sys
from selenium.RunTestCases import RunTestCases
from selenium.RemoteScriptRetriever import RemoteScriptRetriever
import json
import logging
import os


def main():
    allScriptsDict = {}
    # Determine if running a single script or retrieving multiple scripts
    # then store test script in allScriptsDict
    method = str(task.getTaskType())
    if method == "selenium.RunScriptsRetrievedFromRepository":
        scriptRetriever = RemoteScriptRetriever(targetURL, repositoryUsername, repositoryPassword, failIfFileNotFound)
        for key in fileMap:
            allScriptsDict.update({key:scriptRetriever.getData(fileMap[key])})
    elif method == "selenium.RunSinglePythonTestCase":
        allScriptsDict.update({testCaseName:testCase})
        # failOnFirstFailure = True

    # Determine if we will execute scripts remotely and which password to use
    password = ''
    runRemote = False
    if host:
        runRemote = True
        if hostPassword:
            password = hostPassword
        else:
            password = host.get("password")
    if runRemote:
        if method == "selenium.RunScriptsRetrievedFromRepository":
            runner = RunTestCases(allScriptsDict, runRemote, host, password, failOnFirstFailure)
        elif method == "selenium.RunSinglePythonTestCase":
            runner = RunTestCases(allScriptsDict, runRemote, host, password)
    else:
        runner = RunTestCases(allScriptsDict, runRemote)   

    taskOutput, finalExitCode = runner.runTests()

    return taskOutput, finalExitCode


if __name__ == '__main__' or __name__ == '__builtin__':
    reportJson, exitCode = main()
    if exitCode != 0:
        sys.exit(exitCode)











