import popen2, os

class CommandExecutor:
    def run(self, command, display_output=False):
        process =  popen2.Popen4(command)
        res = process.wait()
        if res != 0 or display_output: 
            for line in process.fromchild:
                print line,
        return os.WEXITSTATUS(res)