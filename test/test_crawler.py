import unittest
from unittest.mock import patch
import os
import json
from src.crawler import FileExtractor
import tempfile

class TestFileExtractor(unittest.TestCase):
    
    def test_generate_file_id(self):
        # 創建一個臨時文件來測試
        with open('temp_test_file.txt', 'w') as f:
            f.write('Some test content')

        # 實例化 FileExtractor 並生成文件 ID
        extractor = FileExtractor()
        file_id = extractor.generate_file_id('temp_test_file.txt')

        # 檢查 file_id 是否為預期長度的字符串（SHA-1 雜湊的長度）
        self.assertEqual(len(file_id), 40)

        # 清理臨時文件
        os.remove('temp_test_file.txt')

class TestFileExtractorProcessFiles(unittest.TestCase):

    def setUp(self):
        # 創建一個用於測試的目錄和文件
        os.mkdir('test_dir')
        with open('test_dir/temp_test_file_1.txt', 'w') as f:
            f.write('Test content 1')
        with open('test_dir/temp_test_file_2.txt', 'w') as f:
            f.write('Test content 2')
    
    @unittest.skip("此測試不完善，暫置！")
    def test_process_files(self):
        # 實例化 FileExtractor 並處理文件
        extractor = FileExtractor()
        extractor.local_path = 'test_dir'
        extractor.process_files()

        # 寫入此處您的檢查邏輯，例如檢查是否創建了相應的輸出文件

    def tearDown(self):
        # 清理創建的測試文件和目錄
        os.remove('test_dir/temp_test_file_1.txt')
        os.remove('test_dir/temp_test_file_2.txt')
        os.rmdir('test_dir')

class TestCrawlerFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extractor = FileExtractor()

    def test_extract_text_from_pdf(self):
        # 您需要确保有一個 test.pdf 文件在 test/ 目錄下
        result = self.extractor.extract_text_from_pdf('test/test.pdf')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('page_number', result[0])

    def test_extract_text_from_docx(self):
        # 您需要确保有一個 test.docx 文件在 test/ 目錄下
        result = self.extractor.extract_text_from_docx('test/test.docx')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn('text', result[0])
        self.assertIn('page_number', result[0])

    def test_extract_text_from_xlsx(self):
        # 您需要确保有一個 test.xlsx 文件在 test/ 目錄下
        result = self.extractor.extract_text_from_xlsx('test/test.xlsx')
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for sheet_result in result:
            self.assertIn('sheet_name', sheet_result)
            self.assertIn('contents', sheet_result)

    def test_extract_text_from_txt(self):
        # 您需要确保有一個 test.txt 文件在 test/ 目錄下
        result = self.extractor.extract_text_from_txt('test/test.txt')
        self.assertIsInstance(result, dict)
        self.assertIn('text', result)

class TestWriteToFileFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = [{'text': 'data'*1000}]
        cls.base_filename = 'test_output'
        cls.max_size_mb = 1
        cls.files_created = []
        cls.extractor = FileExtractor()
        cls.directory = 'test/'

    @classmethod
    def tearDownClass(cls):
        for filename in cls.files_created:
            os.remove(filename)

    def test_file_splitting(self):
        # 测试数据是否按照max_size_mb正确分割并写入到多个文件
        self.extractor.write_to_file(self.data, self.directory, self.base_filename, self.max_size_mb)
        # 检查是否创建了多个文件
        file_index = 1
        while True:
            filename = os.path.join(self.directory, f'{self.base_filename}_{file_index}.json')
            if not os.path.exists(filename):
                break
            self.files_created.append(filename)  # 记录文件以便后续删除
            # 确保文件大小小于等于max_size_mb
            self.assertTrue(os.path.getsize(filename) <= self.max_size_mb * 1024 * 1024)
            with open(filename, 'r') as f:
                # 确保文件内容是JSON格式
                content = json.load(f)
                self.assertIsInstance(content, list)  # 内容应为列表格式
                if file_index > 1:
                    # 确保后续文件不是空的
                    self.assertTrue(len(content) > 0)
            file_index += 1

if __name__ == '__main__':
    unittest.main()
