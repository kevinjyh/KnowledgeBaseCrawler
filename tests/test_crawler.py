import unittest
from unittest.mock import patch, MagicMock
from crawler import FileExtractor

class TestFileExtractor(unittest.TestCase):

    @patch('crawler.FileExtractor.load_config')
    def setUp(self, mock_load_config):
        mock_load_config.return_value = {
            "crawl_path": "test",
            "ignore": ["*.txt"],
            "max_size_mb": 1,
            "output_file_name": "output.json"
        }
        self.file_extractor = FileExtractor()

    @patch('os.listdir')
    @patch('json.load')
    def test_load_existing_data(self, mock_json_load, mock_os_listdir):
        mock_os_listdir.return_value = ['output_1.json', 'output_2.json']
        mock_json_load.return_value = [{'file_id': '1'}, {'file_id': '2'}]
        result = self.file_extractor.load_existing_data()
        self.assertEqual(result, [{'file_id': '1'}, {'file_id': '2'}, {'file_id': '1'}, {'file_id': '2'}])

    def test_file_id_exists(self):
        existing_data = [{'file_id': '1'}, {'file_id': '2'}]
        self.assertTrue(self.file_extractor.file_id_exists('1', existing_data))
        self.assertFalse(self.file_extractor.file_id_exists('3', existing_data))

    @patch('crawler.FileExtractor.get_files_in_directory')
    @patch('crawler.FileExtractor.load_existing_data')
    @patch('crawler.FileExtractor.process_all_files')
    @patch('crawler.FileExtractor.write_data_to_files')
    @patch('crawler.FileExtractor.log_updated_files')
    def test_process_files(self, mock_log_updated_files, mock_write_data_to_files, mock_process_all_files, mock_load_existing_data, mock_get_files_in_directory):
        mock_get_files_in_directory.return_value = ['file1', 'file2']
        mock_load_existing_data.return_value = [{'file_id': '1'}, {'file_id': '2'}]
        mock_process_all_files.return_value = ([{'file_id': '3'}], ['file3'])
        self.file_extractor.process_files()
        mock_write_data_to_files.assert_called_once_with([{'file_id': '3'}])
        mock_log_updated_files.assert_called_once_with(['file3'])

    @patch('crawler.FileExtractor.load_config')
    def setUp(self, mock_load_config):
        mock_load_config.return_value = {
            "crawl_path": "test",
            "ignore": ["*.txt"],
            "max_size_mb": 1,
            "output_file_name": "output.json"
        }
        self.file_extractor = FileExtractor()

    @patch('crawler.FileExtractor.process_file')
    def test_process_all_files(self, mock_process_file):
        mock_process_file.side_effect = [{'file_id': '1'}, {'file_id': '2'}]
        result, updated_files = self.file_extractor.process_all_files(['file1', 'file2'])
        self.assertEqual(result, [{'file_id': '1'}, {'file_id': '2'}])
        self.assertEqual(updated_files, ['file1', 'file2'])

    @patch('builtins.open', new_callable=MagicMock)
    def test_write_data_to_files(self, mock_open):
        self.file_extractor.write_data_to_files([{'file_id': '1'}, {'file_id': '2'}])
        mock_open.assert_called_once()

    @patch('builtins.print')
    def test_log_updated_files(self, mock_print):
        self.file_extractor.log_updated_files(['file1', 'file2'])
        mock_print.assert_called()

    @patch('os.path.getctime')
    @patch('os.path.getmtime')
    def test_generate_file_id(self, mock_getmtime, mock_getctime):
        mock_getctime.return_value = 1628000000.0
        mock_getmtime.return_value = 1628000000.0
        result = self.file_extractor.generate_file_id('test.txt')
        self.assertEqual(result, 'edbb0d0f34ed9818bc805b5a09b305a2cbc1110d')

    @patch('crawler.FileExtractor.load_config')
    def setUp(self, mock_load_config):
        mock_load_config.return_value = {
            "crawl_path": "test",
            "ignore": ["*.txt"],
            "max_size_mb": 1,
            "output_file_name": "output.json"
        }
        self.file_extractor = FileExtractor()

    @patch('json.load')
    def test_load_config(self, mock_json_load):
        mock_json_load.return_value = {
            "crawl_path": "test",
            "ignore": ["*.txt"],
            "max_size_mb": 1,
            "output_file_name": "output.json"
        }
        result = self.file_extractor.load_config()
        self.assertEqual(result, {
            "crawl_path": "test",
            "ignore": ["*.txt"],
            "max_size_mb": 1,
            "output_file_name": "output.json"
        })

    @unittest.skip("不知如何將mock_os_listdir傳給被測函式")
    @patch('os.listdir')
    def test_get_files_in_directory(self, mock_os_listdir):
        mock_os_listdir.return_value = ['file1', 'file2']
        result = self.file_extractor.get_files_in_directory(mock_os_listdir)
        self.assertEqual(result, ['file1', 'file2'])

    @patch('builtins.open', new_callable=MagicMock)
    def test_write_to_file(self, mock_open):
        self.file_extractor.write_to_file('output.json', [{'file_id': '1'}, {'file_id': '2'}])
        mock_open.assert_called_once()

    @patch('builtins.print')
    def test_log_process_start(self, mock_print):
        self.file_extractor.log_process_start()
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
    