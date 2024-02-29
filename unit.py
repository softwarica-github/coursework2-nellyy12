import unittest
import tkinter as tk
import os
from mainfim import FileAnalyzer  

class TestFileAnalyzer(unittest.TestCase):
    def setUp(self):
        self.file_path = "test_file.txt"  # Path to a test file
        self.output_text = tk.Text()  

    def test_analyze_added_file(self):
        # Create a test file
        with open(self.file_path, "w") as f:
            f.write("Test content")

        analyzer = FileAnalyzer(self.file_path, self.output_text)
        analyzer.analyze_added_file()

        expected_output = (
            f"Analyzing additions for file: {self.file_path}\n"
            f"- Added {os.path.getsize(self.file_path)} bytes.\n"
            "Addition analysis completed.\n\n"
        ).strip()  # Remove trailing whitespace characters
        self.assertEqual(self.output_text.get("1.0", tk.END).strip(), expected_output)

    def test_analyze_deleted_file(self):
        # Create a test file
        with open(self.file_path, "w") as f:
            f.write("Test content")

        analyzer = FileAnalyzer(self.file_path, self.output_text)
        analyzer.analyze_deleted_file()

        expected_output = (
            f"Analyzing deletions for file: {self.file_path}\n"
            "- Deleted.\n"
            "Deletion analysis completed.\n\n"
        ).strip()  # Remove trailing whitespace characters
        self.assertEqual(self.output_text.get("1.0", tk.END).strip(), expected_output)

    def test_analyze_modified_file(self):
        # Create a test file
        with open(self.file_path, "w") as f:
            f.write("Test content")

        analyzer = FileAnalyzer(self.file_path, self.output_text)
        analyzer.analyze_modified_file()

        expected_output = (
            f"Analyzing modifications for file: {self.file_path}\n"
            "- Modified.\n"
            "Modification analysis completed.\n\n"
        ).strip()  # Remove trailing whitespace characters
        self.assertEqual(self.output_text.get("1.0", tk.END).strip(), expected_output)

if __name__ == "__main__":
    unittest.main()
