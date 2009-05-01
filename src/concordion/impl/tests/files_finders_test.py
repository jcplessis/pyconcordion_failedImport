import unittest
import os, shutil
from concordion.impl.files_finders import FolderTestFinder

class FolderRunnerTest(unittest.TestCase):
    example_folder = "example_folder"
    
    def setUp(self):
        os.mkdir(self.example_folder)
        
    def tearDown(self):
        shutil.rmtree(self.example_folder)
        
    def test_creation_saves_folder_name(self):
        "Folder Finder - saves the given folder name"
        runner = FolderTestFinder("folder_name")
        self.assertEquals("folder_name", runner.folder)

    def test_can_find_py_files_directly_under_folder(self):
        "Folder Finder - can find py files directly under given folder"
        self._create_file("fileTest.py")
        self._create_file("not_interesting.txt")
        runner = FolderTestFinder("./example_folder")
        py_files = runner.find_files()
        self.assertEquals(1, len(py_files))
        self.assertEquals("./example_folder/fileTest.py", py_files[0])
        
    def test_can_find_py_files_recursively(self):
        "Folder Finder - can find py files recursively"
        self._create_file("polop_folder/fileTest.py")
        runner = FolderTestFinder("example_folder")
        py_files = runner.find_files()
        self.assertEquals(1, len(py_files))
        self.assertEquals("example_folder/polop_folder/fileTest.py", py_files[0])    
    
    
    def test_dont_search_in_svn_directory(self):
        "Folder Finder - does not search in directories starting with a dot"
        self._create_file("polop_folder/fileTest.py")
        self._create_file(".svn/otherFileTest.py")
        runner = FolderTestFinder("example_folder")
        py_files = runner.find_files()
        self.assertEquals(1, len(py_files))
        self.assertEquals("example_folder/polop_folder/fileTest.py", py_files[0])    
        
    def _create_file(self, filepath):
        directory, file = os.path.split(filepath)
        parent_folder = os.path.join(self.example_folder, directory)
        if not os.path.exists(parent_folder):
            os.mkdir(parent_folder)
        full_path = os.path.join(self.example_folder, filepath)
        open(full_path, "w").close()
        
        
