import unittest
from concordion.impl.runners import TestRunner
import pmock

class TestRunnerTest(unittest.TestCase):
    
    def test_asks_files_to_filefinder_and_runs_executor(self):
        "Test Runner - Asks for files to FileFinder and runs TestExecutor"
        file_finder = pmock.Mock()
        file_finder.expects(pmock.once()).find_files().will(pmock.return_value(['polop.py']))
        executor = pmock.Mock()
        executor.expects(pmock.once()).run(pmock.eq(['polop.py']))
        TestRunner(file_finder, executor).run()
        file_finder.verify()
        executor.verify()
