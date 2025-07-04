import unittest

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


class GetFilesInfoTest(unittest.TestCase):
    def test_CWD(self):
        output = get_files_info("calculator", ".")
        self.assertFalse(output.startswith("Error:"))
        print(output)

    def test_pkg(self):
        output = get_files_info("calculator", "pkg")
        self.assertFalse(output.startswith("Error:"))
        print(output)

    def test_bin(self):
        output = get_files_info("calculator", "/bin")
        self.assertTrue(output.startswith("Error:"))
        print(output)

    def test_parent(self):
        output = get_files_info("calculator", "../")
        self.assertTrue(output.startswith("Error:"))
        print(output)


class GetFilesContentTest(unittest.TestCase):
    def test_parent(self):
        content = get_file_content("calculator", "../")
        self.assertTrue(content.startswith("Error:"))
        print(content)

    def test_main(self):
        content = get_file_content("calculator", "main.py")
        self.assertFalse(content.startswith("Error:"))
        print(content)

    def test_calculator(self):
        content = get_file_content("calculator", "pkg/calculator.py")
        self.assertFalse(content.startswith("Error:"))
        print(content)

    def test_bin(self):
        content = get_file_content("calculator", "/bin/cat")
        self.assertTrue(content.startswith("Error:"))
        print(content)

    def test_lorem_long(self):
        content = get_file_content("calculator", "lorem_long.txt")
        self.assertTrue(
            content.endswith(
                '[...File "lorem_long.txt" truncated at 10_000 characters]'
            )
        )
        print(content)


class WriteFilesContentTest(unittest.TestCase):
    def test_parent(self):
        output = write_file("calculator", "../", "this should not be allowed")
        self.assertTrue(output.startswith("Error:"))
        print(output)

    def test_lorem(self):
        output = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        self.assertFalse(output.startswith("Error:"))
        print(output)

    def test_more_lorem(self):
        output = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        self.assertFalse(output.startswith("Error:"))
        print(output)

    def test_root_outside(self):
        output = write_file(
            "calculator", "/tmp/temp.txt", "wait, this should not be allowed"
        )
        self.assertTrue(output.startswith("Error:"))
        print(output)


class RunPythonFileTest(unittest.TestCase):
    def test_parent(self):
        output = run_python_file("calculator", "../main.py")
        self.assertTrue(output.startswith("Error:"))
        print(output)

    def test_calculator_tests(self):
        output = run_python_file("calculator", "tests.py")
        self.assertFalse(output.startswith("Error:"))
        print(output)

    def test_calculator_main(self):
        output = run_python_file("calculator", "main.py")
        self.assertFalse(output.startswith("Error:"))
        print(output)

    def test_nonexistent_file(self):
        output = run_python_file("calculator", "nonexistent.py")
        self.assertTrue(output.startswith("Error:"))
        print(output)


if __name__ == "__main__":
    unittest.main()
