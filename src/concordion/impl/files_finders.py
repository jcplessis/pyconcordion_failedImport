import sys, os, re

class FolderTestFinder:
    def __init__(self, params):
        if len(params) != 2:
            print "Usage : %s FOLDER"%params[0]
            sys.exit(1)
        self.folder = params[1]
    
    def find_files(self):
        python_matcher = re.compile("\.py")
        result = []
        for root, dirs, files in os.walk(self.folder):
            result.extend([os.path.join(root, f) for f in files if python_matcher.findall(f)])
        return result