import unittest
from concordion.impl.executors import CommandExecutor

class CommandExecutorTest(unittest.TestCase):
    
    def testCanRunASimpleCommand(self):
        "Executor - Can run a simple command"
        self.assertEquals(0, CommandExecutor().run("echo Hello world !"))
        
    def testCanRunACommandReturning1(self):
        "Executor - Can run a command returning 1"
        self.assertEquals(1, CommandExecutor().run("exit 1"))
        
