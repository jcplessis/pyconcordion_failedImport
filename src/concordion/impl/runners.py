

class TestRunner:
    
    def __init__(self, file_finder, test_executor):
        self.file_finder = file_finder
        self.test_executor = test_executor
    
    def run(self):
        self.test_executor.run(self.file_finder.find_files())