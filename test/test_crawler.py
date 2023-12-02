
import sys
from pathlib import Path

# 確保將 src 目錄添加到 sys.path 中
current_dir = Path(__file__).parent
src_dir = current_dir.parent / 'src'
test_dir = current_dir.parent / 'test'
sys.path.append(str(src_dir))
sys.path.append(str(test_dir))

import unittest
from crawler import extract_text_from_pdf, extract_text_from_docx, extract_text_from_xlsx, extract_text_from_txt, get_local_file_content

class TestCrawlerFunctions(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        # 您需要确保有一個 test.pdf 文件在 test/ 目錄下
        result = extract_text_from_pdf('test/test.pdf')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('page_number', result[0])

    def test_extract_text_from_docx(self):
        # 您需要确保有一個 test.docx 文件在 test/ 目錄下
        result = extract_text_from_docx('test/test.docx')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('page_number', result[0])

    def test_extract_text_from_xlsx(self):
        # 您需要确保有一個 test.xlsx 文件在 test/ 目錄下
        result = extract_text_from_xlsx('test/test.xlsx')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for sheet_result in result:
            self.assertIn('sheet_name', sheet_result)
            self.assertIn('contents', sheet_result)

    def test_extract_text_from_txt(self):
        # 您需要确保有一個 test.txt 文件在 test/ 目錄下
        result = extract_text_from_txt('test/test.txt')
        self.assertIsInstance(result, dict)
        self.assertIn('text', result)

if __name__ == '__main__':
    unittest.main()
