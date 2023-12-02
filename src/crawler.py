
import os
import json
import pdfplumber
from docx import Document
import openpyxl
import fnmatch

# 獲取當前腳本的絕對路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.json')

# 載入配置文件
with open(config_path, 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

# 從配置文件中獲取變量值
local_path = config["local_path"]
output_file_name = config["output_file_name"]
ignore_patterns = config["ignore"]
max_size_mb = config["max_size_mb"]

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return [{'text': page.extract_text(), 'page_number': i+1} for i, page in enumerate(pdf.pages) if page.extract_text()]

def extract_tables_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        tables = []
        for page in pdf.pages:
            page_tables = page.extract_tables()
            for table in page_tables:
                tables.append([row for row in table])
        return tables

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return [{'text': paragraph.text, 'page_number': i+1} for i, paragraph in enumerate(doc.paragraphs) if paragraph.text]

def extract_tables_from_docx(file_path):
    doc = Document(file_path)
    tables = []
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                row_data.append(cell.text.strip())
            table_data.append(row_data)
        tables.append(table_data)
    return tables

def extract_text_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path, read_only=True)
    return [{'sheet_name': sheet.title, 'contents': '\n'.join(cell.value if cell.value is not None else '' for row in sheet for cell in row)} for sheet in workbook.worksheets]

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return {'text': file.read()}

def get_local_file_content(file_path):
    print(f"Crawling {file_path}")

    # 獲取完整的檔案路徑
    full_path = os.path.abspath(file_path)
    file_extension = os.path.splitext(file_path)[1].lower().lstrip('.')
    content = {'text': [], 'tables': []}
    
    if file_extension in ['pdf']:
        content['text'] = extract_text_from_pdf(full_path)
        content['tables'] = extract_tables_from_pdf(full_path)
    elif file_extension in ['docx', 'doc']:
        content['text'] = extract_text_from_docx(full_path)
        content['tables'] = extract_tables_from_docx(full_path)
    elif file_extension in ['xlsx', 'xls']:
        content = extract_text_from_xlsx(full_path)
    elif file_extension in ['txt', 'md', 'html']:
        content = extract_text_from_txt(full_path)
    else:
        content = None  # f"****尚未支援{file_extension}類型的檔案****"
    
    return {
        'file_path': full_path,  # 使用完整路徑
        'content': content
    }

def get_files_in_directory(directory_path, ignore_patterns):
    """获取指定目录及其子目录下的所有文件名, 排除ignore_patterns中指定的模式"""
    files = []
    for root, dirs, files_in_dir in os.walk(directory_path):
        for filename in files_in_dir:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path) and not any(fnmatch.fnmatch(filename, pattern) for pattern in ignore_patterns):
                files.append(file_path)
    return files


# 使用 get_files_in_directory 函数来生成檔案列表
list_of_files_to_crawl = get_files_in_directory(local_path, ignore_patterns)

def write_to_file(data, base_filename, max_size_mb, encoding='utf-8'):
    # 初始文件索引
    file_index = 1
    # 数据分块大小
    chunk_size = 1024 * 1024 * max_size_mb # 将MB转换为字节
    # 初始化当前块
    current_chunk = []
    current_size = 0
    
    for item in data:
        item_size = len(json.dumps(item, ensure_ascii=False).encode(encoding))
        if current_size + item_size > chunk_size:
            # 当前块的大小已经超过限制，写入文件
            filename = f'{base_filename}_{file_index}.json'
            with open(filename, 'w', encoding=encoding) as f:
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
        with open(filename, 'w', encoding=encoding) as f:
            json.dump(current_chunk, f, ensure_ascii=False, indent=4)

# 爬取文件并保存结果
crawled_data = []
for file_path in list_of_files_to_crawl:
    file_contents = get_local_file_content(file_path)
    crawled_data.append(file_contents)

# 写入文件
base_output_file_name = os.path.splitext(output_file_name)[0]  # 不包含副檔名
write_to_file(crawled_data, base_output_file_name, max_size_mb)