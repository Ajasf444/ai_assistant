import unittest
from functions.get_files_info import get_files_info


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


if __name__ == "__main__":
    unittest.main()
