
import unittest
from your_crawler_script import extract_text_from_pdf, extract_text_from_docx, extract_text_from_xlsx, get_local_file_content

class TestCrawler(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        result = extract_text_from_pdf('test.pdf')
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], str)

    def test_extract_text_from_docx(self):
        result = extract_text_from_docx('test.docx')
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], str)

    def test_extract_text_from_xlsx(self):
        result = extract_text_from_xlsx('test.xlsx')
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIsInstance(result[0], str)

    def test_get_local_file_content(self):
        for file_path in ['test.pdf', 'test.docx', 'test.xlsx', 'test.txt']:
            result = get_local_file_content(file_path)
            self.assertIsInstance(result, list)
            self.assertTrue(len(result) > 0)
            self.assertIn('text', result[0])
            self.assertIn('line_number', result[0] or 'page_number' in result[0] or 'cell_number' in result[0])

if __name__ == '__main__':
    unittest.main()
