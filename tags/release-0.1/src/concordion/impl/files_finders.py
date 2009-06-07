import sys, os, re

class FolderTestFinder:
    def __init__(self, folder):
        self.folder = folder
    
    def find_files(self):
        python_matcher = re.compile("\.py$")
        hidden_folder_matcher = re.compile("\.[^/]")
        result = []
        for root, dirs, files in os.walk(self.folder):
            if not hidden_folder_matcher.findall(root):
                result.extend([os.path.join(root, f) for f in files if python_matcher.findall(f)])
        return result