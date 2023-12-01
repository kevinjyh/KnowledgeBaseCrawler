
import os
import json
import pdfplumber
from docx import Document
import openpyxl

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return [page.extract_text() for page in pdf.pages]

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return [paragraph.text for paragraph in doc.paragraphs if paragraph.text]

def extract_text_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(file_path, read_only=True)
    sheet = workbook.active
    return [cell.value for row in sheet for cell in row if cell.value]

def get_local_file_content(file_path):
    print(f"Crawling {file_path}")

    file_contents = []
    if file_path.endswith('.pdf'):
        text_pages = extract_text_from_pdf(file_path)
        for page_number, page_text in enumerate(text_pages, start=1):
            if page_text:
                file_contents.append({
                    'text': page_text,
                    'page_number': page_number
                })
    elif file_path.endswith('.docx'):
        for i, text in enumerate(extract_text_from_docx(file_path)):
            file_contents.append({
                'text': text,
                'line_number': i + 1
            })
    elif file_path.endswith('.xlsx'):
        for i, text in enumerate(extract_text_from_xlsx(file_path)):
            file_contents.append({
                'text': text,
                'cell_number': i + 1
            })
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                file_contents.append({
                    'text': line.strip(),
                    'line_number': i + 1
                })

    return file_contents

# 示例文件列表
list_of_files_to_crawl = ['example.docx', 'example.xlsx', 'example.pdf', 'example.txt']

# 爬取文件並保存結果
crawled_data = []
for file_path in list_of_files_to_crawl:
    crawled_data.append({
        'file_path': file_path,
        'contents': get_local_file_content(file_path)
    })

with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(crawled_data, f, ensure_ascii=False, indent=4)
