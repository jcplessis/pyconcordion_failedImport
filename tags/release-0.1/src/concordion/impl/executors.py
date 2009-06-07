import subprocess

class CommandExecutor:
    def run(self, command, display_output=False):
        process =  subprocess.Popen(command, shell=True,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        res = process.wait()
        if res != 0 or display_output: 
            for line in process.stdout:
                print line,
        return res