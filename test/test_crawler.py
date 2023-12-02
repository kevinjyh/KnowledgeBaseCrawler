
import json
import os
import unittest
from src.crawler import write_to_file, extract_text_from_pdf, extract_text_from_docx, extract_text_from_xlsx, extract_text_from_txt, get_local_file_content

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

class TestWriteToFileFunction(unittest.TestCase):

    def setUp(self):
        # 设置测试数据和测试文件名
        self.data = [{'text': 'data'*1000}]  # 重复的数据以产生足够大的大小
        self.base_filename = 'test_output'
        self.max_size_mb = 1  # 设置文件大小的上限为1MB，便于测试
        self.files_created = []  # 用于记录创建的测试文件

    def tearDown(self):
        # 测试结束后删除所有创建的测试文件
        for filename in self.files_created:
            os.remove(filename)

    def test_file_splitting(self):
        # 测试数据是否按照max_size_mb正确分割并写入到多个文件
        write_to_file(self.data, self.base_filename, self.max_size_mb)
        # 检查是否创建了多个文件
        file_index = 1
        while True:
            filename = f'{self.base_filename}_{file_index}.json'
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

        # 确保至少创建了两个文件（假设数据足够大）
        # self.assertTrue(file_index > 2)

if __name__ == '__main__':
    unittest.main()
