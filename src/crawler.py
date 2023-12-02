
import os
import json
import pdfplumber
from docx import Document
import openpyxl

# 將支援的擴展名設為全局變量
supported_extensions = ['pdf', 'docx', 'doc', 'xlsx', 'xls', 'txt', 'md', 'html']


def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return [{'text': page.extract_text(), 'page_number': i+1} for i, page in enumerate(pdf.pages) if page.extract_text()]

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return [{'text': paragraph.text, 'page_number': i+1} for i, paragraph in enumerate(doc.paragraphs) if paragraph.text]

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
    content = None
    
    if file_extension in supported_extensions:
        if file_extension in ['pdf']:
            content = extract_text_from_pdf(full_path)
        elif file_extension in ['docx', 'doc']:
            content = extract_text_from_docx(full_path)
        elif file_extension in ['xlsx', 'xls']:
            content = extract_text_from_xlsx(full_path)
        elif file_extension in ['txt', 'md', 'html']:
            content = extract_text_from_txt(full_path)
    else:
        content = f"****尚未支援{file_extension}類型的檔案****"
    
    return {
        'file_path': full_path,  # 使用完整路徑
        'content': content
    }

def get_files_in_directory(directory_path):
    """獲取指定目錄下的所有檔案名稱"""
    files = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            files.append(os.path.join(directory_path, filename))
    return files

# 使用 get_files_in_directory 函数来生成檔案列表
test_directory_path = 'test/'
list_of_files_to_crawl = get_files_in_directory(test_directory_path)

# 爬取文件並保存結果
crawled_data = []
for file_path in list_of_files_to_crawl:
    file_contents = get_local_file_content(file_path)
    crawled_data.append(file_contents)

# 將結果保存為 JSON 檔案
output_file_path = 'KB.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(crawled_data, f, ensure_ascii=False, indent=4)
