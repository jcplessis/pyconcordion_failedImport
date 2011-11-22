import subprocess
import sys

class CommandExecutor:
	def run(self, command, display_output=False):
		process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=sys.stdout)
		return process.wait()
