import sys, json, __builtin__

from com.xebialabs.overthere import CmdLine, ConnectionOptions, OperatingSystemFamily, Overthere
from com.xebialabs.overthere.ssh import SshConnectionBuilder, SshConnectionType
from com.xebialabs.overthere.local import LocalConnection
from com.xebialabs.overthere.util import CapturingOverthereExecutionOutputHandler, OverthereUtils
from java.io import StringWriter, PrintWriter
from java.lang import String

class SeleniumRunner():
    def __init__(self, script, connectionType=None, host=None, password=None):
        self.logger = getattr(__builtin__, 'logger', None)
        self.script = script
        
        self.connectionType = connectionType

        if host:
            self.options = ConnectionOptions()
            self.options.set(ConnectionOptions.USERNAME, host.getProperty('username'))
            self.options.set(ConnectionOptions.PASSWORD, password)
            self.options.set(ConnectionOptions.ADDRESS, host.getProperty('address'))
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
        except Error, e:
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