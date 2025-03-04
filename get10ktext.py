from bs4 import BeautifulSoup
import re
import chardet

def detect_file_encoding(file_path):
    """
    检测文件的编码格式。
    """
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result["encoding"]

def extract_item_7(html_content):
    """
    从 HTML 内容中提取 "Item 7: Management's Discussion and Analysis" 部分。
    """
    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 获取所有文本内容
    text = soup.get_text(separator="\n")
    
    # 定义正则表达式匹配 Item 7 部分
    item_7_pattern = re.compile(
        r"Item\s*7[\.\s]*Management['’]s\s*Discussion\s*and\s*Analysis\s*of\s*Financial\s*Condition\s*and\s*Results\s*of\s*Operations\s*The.*?"
        r"Item\s*7A",
        # r"(Item\s*7A|\bItem\s*8\b)",
        re.IGNORECASE | re.DOTALL
    )
    
    # 查找 Item 7 部分
    match = item_7_pattern.search(text)
    if match:
        return match.group(0).strip()
    else:
        return "Item 7 not found in the document."

def save_to_txt(content, output_path):
    """
    将内容保存到 TXT 文件。
    """
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

# 本地 HTML 文件路径
html_file_path = "C:/Users/73149/Desktop/Uncertainty/files_10k/10-K.html"

# 输出 TXT 文件路径
output_txt_path = "C:/Users/73149/Desktop/Uncertainty/files_10k/Item7.txt"

# 检测文件编码
encoding = detect_file_encoding(html_file_path)
print(f"检测到的文件编码: {encoding}")

# 使用检测到的编码读取 HTML 文件内容
with open(html_file_path, "r", encoding=encoding) as file:
    html_content = file.read()

# 提取 Item 7 部分
item_7_text = extract_item_7(html_content)

# 保存到 TXT 文件
save_to_txt(item_7_text, output_txt_path)

print(f"Item 7 部分已提取并保存到: {output_txt_path}")
