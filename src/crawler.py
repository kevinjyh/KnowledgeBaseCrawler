# crawler.py
import concurrent.futures
import hashlib
import os
import logging
from datetime import datetime
import threading
from functools import lru_cache
import json
import fnmatch
from content import ContentExtractor  # 導入 ContentExtractor

class FileExtractor:
    def __init__(self, config_path='src/config.json'):
        self.content_extractor = ContentExtractor()
        self.config = self.load_config(config_path)
        self.crawl_path = self.config["crawl_path"]
        self.ignore_patterns = self.config["ignore"]
        self.max_size_mb = self.config["max_size_mb"]
        self.base_output_file_name = os.path.splitext(self.config["output_file_name"])[0]  # 不包含副檔名
        # 初始化緩存大小和鎖
        self.file_id_cache = lru_cache(maxsize=10000)
        self.lock = threading.Lock()
        # 設置日誌
        logging.basicConfig(filename='src/updated.log',  # 根目錄下的日誌文件
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def load_existing_data(self):
        existing_data = []
        # 获取当前脚本文件所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 在当前目录下搜索 JSON 文件
        for filename in os.listdir(current_dir):
            if filename.startswith(self.base_output_file_name + '_') and filename.endswith(".json"):
                # 使用当前目录和文件名构造完整的文件路径
                file_path = os.path.join(current_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    existing_data.extend(data)
        return existing_data

    def file_id_exists(self, file_id, existing_data):
        return any(item['file_id'] == file_id for item in existing_data)

    def process_files(self):
        files_to_process = self.get_files_in_directory(self.crawl_path)
        existing_data = self.load_existing_data()
        crawled_data, updated_files = self.process_all_files(files_to_process, existing_data)
        self.write_data_to_files(crawled_data)
        self.log_updated_files(updated_files)

    def process_all_files(self, files, existing_data):
        crawled_data = []
        updated_files = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.content_extractor.get_local_file_content, file): file for file in files}
            for future in concurrent.futures.as_completed(futures):
                file = futures[future]
                try:
                    data = future.result()
                    if not self.file_id_exists(data['file_id'], existing_data):
                        print(f"Crawling {file}")
                        crawled_data.append(data)
                        updated_files.append(file)
                    else:
                        print('.', end='')
                except Exception as exc:
                    logging.error(f'File processing generated an exception: {file}, {exc}')
        return crawled_data, updated_files

    def write_data_to_files(self, crawled_data):
        if crawled_data:
            self.write_to_file(crawled_data, None, self.base_output_file_name, self.max_size_mb)

    def log_updated_files(self, updated_files):
        for file in updated_files:
            logging.info(f'更新檔案：{file}')

    @staticmethod
    # @lru_cache(maxsize=10000)
    def generate_file_id(file_path):
        try:
            # 獲取文件的絕對路徑、創建日期和修改日期
            absolute_path = os.path.abspath(file_path)
            creation_time = os.path.getctime(file_path)
            modification_time = os.path.getmtime(file_path)
            # 串聯這些信息
            data = f"{absolute_path}{creation_time}{modification_time}"
            # 使用 SHA-1 生成雜湊
            return hashlib.sha1(data.encode()).hexdigest()
        except Exception as e:
            print(f"Error generating file ID for {file_path}: {e}")
            return None

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)

    def get_files_in_directory(self, directory_path):
        files = []
        for root, dirs, files_in_dir in os.walk(directory_path):
            for filename in files_in_dir:
                file_path = os.path.join(root, filename)
                if os.path.isfile(file_path) and not any(fnmatch.fnmatch(filename, pattern) for pattern in self.ignore_patterns):
                    files.append(file_path)
        return files

    def write_to_file(self, data, directory, base_filename, max_size_mb, encoding='utf-8'):
        if directory is None:
            directory = os.path.dirname(os.path.abspath(__file__))

        # 初始文件索引
        file_index = 1
        # 数据分块大小
        chunk_size = 1024 * 1024 * max_size_mb  # 将MB转换为字节
        # 初始化当前块
        current_chunk = []
        current_size = 0

        for item in data:
            item_size = len(json.dumps(item, ensure_ascii=False).encode(encoding))
            if current_size + item_size > chunk_size:
                # 当前块的大小已经超过限制，写入文件
                filename = f'{base_filename}_{file_index}.json'
                full_path = os.path.join(directory, filename)  # 构建完整的文件路径
                with open(full_path, 'w', encoding=encoding) as f:
                    json.dump(current_chunk, f, ensure_ascii=False, indent=4)
                # 重置当前块和大小计数器
                current_chunk = [item]
                current_size = item_size
                file_index += 1
            else:
                # 将当前项目添加到块中
                current_chunk.append(item)
                current_size += item_size

        # 写入最后一个文件（如果有剩余数据）
        if current_chunk:
            filename = f'{base_filename}_{file_index}.json'
            full_path = os.path.join(directory, filename)  # 构建完整的文件路径
            with open(full_path, 'w', encoding=encoding) as f:
                json.dump(current_chunk, f, ensure_ascii=False, indent=4)

    def log_process_start(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        separator = '=' * 20 + f' {current_time} ' + '=' * 20
        logging.info(separator)

    def crawl(self):
        self.log_process_start()
        self.process_files()


# Main execution
if __name__ == "__main__":
    FileExtractor().crawl()
    