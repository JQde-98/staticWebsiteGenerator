import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_simple_title(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_title_with_spaces(self):
        markdown = "#    Lots of Spaces    "
        self.assertEqual(extract_title(markdown), "Lots of Spaces")
    
    def test_multiline_markdown(self):
        markdown = "# The Title\n\nThis is some content.\n\n## Subtitle"
        self.assertEqual(extract_title(markdown), "The Title")
    
    def test_no_title(self):
        markdown = "This is just text without a title"
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_title_not_at_beginning(self):
        markdown = "Some text\n# Title"
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()