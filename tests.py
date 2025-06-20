import unittest
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content


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
    def test_outside(self):
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

    def test_lorem(self):
        content = get_file_content("calculator", "lorem.txt")
        self.assertTrue(
            content.endswith(
                '[...File "lorem.txt" truncated at 10_000 characters]')
        )
        print(content)


if __name__ == "__main__":
    unittest.main()
