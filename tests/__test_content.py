# FILEPATH: /c:/Users/user/我的雲端硬碟/KnowledgeBaseCrawler/test/test_content.py

import unittest
from unittest.mock import patch, MagicMock
from content import ContentExtractor

class TestContentExtractor(unittest.TestCase):

    @patch('content.ContentExtractor.extract_text_from_pdf')
    @patch('content.ContentExtractor.extract_tables_from_pdf')
    def test_get_local_file_content_pdf(self, mock_extract_text, mock_extract_tables):
        mock_extract_text.return_value = ['text']
        mock_extract_tables.return_value = ['table']
        extractor = ContentExtractor()
        result = extractor.get_local_file_content('test.pdf')
        self.assertEqual(result['content']['text'], ['text'])
        self.assertEqual(result['content']['tables'], ['table'])

    @patch('content.ContentExtractor.extract_text_from_docx')
    @patch('content.ContentExtractor.extract_tables_from_docx')
    def test_get_local_file_content_docx(self, mock_extract_text, mock_extract_tables):
        mock_extract_text.return_value = ['text']
        mock_extract_tables.return_value = ['table']
        extractor = ContentExtractor()
        result = extractor.get_local_file_content('test.docx')
        self.assertEqual(result['content']['text'], ['text'])
        self.assertEqual(result['content']['tables'], ['table'])

    @patch('content.ContentExtractor.extract_text_from_xlsx')
    def test_get_local_file_content_xlsx(self, mock_extract_text):
        mock_extract_text.return_value = ['text']
        extractor = ContentExtractor()
        result = extractor.get_local_file_content('test.xlsx')
        self.assertEqual(result['content'], ['text'])

    @patch('content.ContentExtractor.extract_text_from_txt')
    def test_get_local_file_content_txt(self, mock_extract_text):
        mock_extract_text.return_value = {'text': 'text'}
        extractor = ContentExtractor()
        result = extractor.get_local_file_content('test.txt')
        self.assertEqual(result['content'], {'text': 'text'})

if __name__ == '__main__':
    unittest.main()