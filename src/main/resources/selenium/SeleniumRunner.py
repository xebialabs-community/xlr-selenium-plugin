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

from com.xebialabs.overthere import CmdLine, ConnectionOptions, OperatingSystemFamily, Overthere
from com.xebialabs.overthere.ssh import SshConnectionBuilder, SshConnectionType
from com.xebialabs.overthere.local import LocalConnection
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from java.io import StringWriter, PrintWriter
from java.lang import String
import logging

logger = logging.getLogger(__name__)

class SeleniumRunner():
    def __init__(self, script, connectionType=None, host=None, password=None):
        self.logger = logger
        # self.logger.debug("In Selenium Runner init")
        self.script = script
        
        self.connectionType = connectionType

        if host:
            self.options = ConnectionOptions()
            self.options.set(ConnectionOptions.USERNAME, host.get("username"))
            self.options.set(ConnectionOptions.PASSWORD, password)
            self.options.set(ConnectionOptions.ADDRESS, host.get("address"))
            self.options.set(ConnectionOptions.OPERATING_SYSTEM, OperatingSystemFamily.UNIX)
            self.options.set(SshConnectionBuilder.CONNECTION_TYPE, SshConnectionType.SCP)
        else:
            self.options = None

        self.stdout = CapturingOverthereExecutionOutputHandler.capturingHandler()
        self.stderr = CapturingOverthereExecutionOutputHandler.capturingHandler()      

    def execute(self):
        connection = None
        try:
            connection = self.getConnection()
            # upload the script and pass it to python
            exeFile = connection.getTempFile('script', '.py')
            OverthereUtils.write(String(self.script).getBytes(), exeFile)
            exeFile.setExecutable(True)
            scriptCommand = CmdLine.build( '/usr/bin/python', exeFile.getPath() )
            return connection.execute(self.stdout, self.stderr, scriptCommand)
        except AttributeError, e:
            self.logger.error(str(e))
        except NameError, e:
            self.logger.error(str(e))
        except Exception, e:
            stacktrace = StringWriter()
            writer = PrintWriter(stacktrace, True)
            e.printStackTrace(writer)
            self.stderr.handleLine(stacktrace.toString())
            return 1
        finally:
            if connection is not None:
                connection.close()

    def getConnection(self):
        if (self.connectionType):
            return Overthere.getConnection("ssh", self.options)
        else:
            return LocalConnection.getLocalConnection()

    def getStdout(self):
        return self.stdout.getOutput()

    def getStdoutLines(self):
        return self.stdout.getOutputLines()

    def getStderr(self):
        return self.stderr.getOutput()

    def getStderrLines(self):
        return self.stderr.getOutputLines()