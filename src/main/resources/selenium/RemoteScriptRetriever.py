#
# Copyright 2020 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import os.path
import urllib2, base64
import sys
import logging

logger = logging.getLogger(__name__)

class RemoteScriptRetriever():
    def __init__(self, targetURL, repositoryUsername, repositoryPassword, failIfFileNotFound):
        self.logger = logger
        self.repositoryUsername = repositoryUsername
        self.repositoryPassword = repositoryPassword
        self.failIfFileNotFound = failIfFileNotFound
        self.targetURL = targetURL
        self.logger.debug("targertURL = %s, repositoryUsername=%s,  failIfFileNotFound=%s" %
            (targetURL, repositoryUsername, str(failIfFileNotFound)))
    

    def getData(self, fileName):
        base64string = base64.b64encode('%s:%s' % (self.repositoryUsername, self.repositoryPassword)).replace('\n', '')
        url = self.targetURL.replace(":filename:", fileName)
        self.logger.debug("The complete url = %s" % url)
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)
        data = ""
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e, 'reason'):
                self.logger.debug('Failed to reach server - Reason: %s'% e.reason)
            if hasattr(e, 'code'):
                self.logger.debug('The server did not fulfill the request - Code: %s'% str(e.code))

            # If user has configured for failure if a file is not retrieved
            if self.failIfFileNotFound:
                self.logger.debug('File Not Found: %s'% url)
                print ("File not found - %s" % url)
                sys.exit(1)
            else:
                return data
        else:
            data = response.read(200000) # read up to 200 000 chars 
        return data


